import aiohttp
from constants import STATUS_DOWNLOAD_FILE ,SAVE_DIR ,idm_status,SAVE_STATE_FILE
# import constants
import time
import asyncio
import requests
import bson
import os
import aiofiles

    
# getting new speed
async def update_item_speed(local_file_status,session,init_test_size=1024*100,interval=0.2):

    if not local_file_status:
        return local_file_status
    url=local_file_status.get('Url',None)
    
    headers = {'Range': f'bytes=0-{init_test_size-1}'}
    receivedData=0
    start_time = time.time()
    test_size_bytes = init_test_size
    print("update_item_speed  💃💃💃💃💃💃💃")
    
    async with session.get(url, headers=headers) as response:
        while True:
            try:
                # async for chunk in response.content.iter_chunked(1024):
                # Attempt to read exactly test_size_bytes
                chunk = await asyncio.wait_for(response.content.readexactly(test_size_bytes), timeout=5)
                receivedData=len(chunk)
                break  # Success, exit the loop
            except Exception as e:
                factor+=1
                # Reduce test_size_bytes if readexactly fails
                test_size_bytes -= 1024  # Example reduction, adjust as needed
                if test_size_bytes <= 50000:
                    local_file_status['Speed']=10000
                    break

        end_time = time.time()
        elapsed_time = end_time - start_time
        speed_in_bytes_per_second = receivedData / elapsed_time
        rounded_speed = round(speed_in_bytes_per_second)
        local_file_status['Speed']=rounded_speed
        return local_file_status

# loop through active downloads and try to update their down speed
async def handle_update_speed(updated_statuses,session):
    print(f"handle_update_speed started  😄😄😄😄😄😄😄😄😄 length {len(updated_statuses)}")
    
    while updated_statuses:
        print("speed start updating 🇵🇬🇵🇬🇵🇬🇵🇬🇵🇬🇵🇬")
        if not idm_status.bandwidth_queue.empty():
            print("speed before block💚💚💚💚💚")
            file_name, action, status_data = await idm_status.bandwidth_queue.get()
            print("speed received  bandwidth request")
            if action == "add":
                updated_statuses[file_name] = status_data  # Add/update status
            elif action == "remove":
                updated_statuses.pop(file_name, None)  # Remove if exists
                # idm_status.bandwidth_queue.task_done()

        # if updated_statuses:
        # Update speed for tracked files
        for name in updated_statuses.keys():
            print(f"🍓each updating speed for --------- {name}")
            # add status check if is False remove this key from updated_statuses
            updated_statuses[name] = await update_item_speed(updated_statuses[name],session)

            # updated_statuses[name] = await update_singleitem_speed(updated_statuses[name],session)
        await idm_status.status_queue.put((None, updated_statuses))
        
        await asyncio.sleep(2)
        print("handle_update_speed ended  😄😄😄😄😄😄😄😄😄")

# routine for updating speed of active downloads
async def update_bandwidth_speed():
    """Continuously updates the speed of tracked downloads."""
    updated_statuses = {}  # Stores active downloads and their status
    while True:
        print("speed is updating wating for triger 🇵🇬🇵🇬😀🇵🇬🇵🇬🇵🇬🇵🇬")
        file_name, action, status_data = await idm_status.bandwidth_queue.get()
        if not updated_statuses:
            updated_statuses[file_name] = status_data  # Add/update status
            session=idm_status.open_session
            await handle_update_speed(updated_statuses,session)

async def session_manager():
    """Manages the session lifecycle using an event trigger."""
    while True:
        # Wait for a signal to start the session
        await idm_status.session_event.wait()
        async with idm_status.status_lock:
            active_downloads = any(file_data['Status'] for file_data in idm_status.status_track.values())
            if not active_downloads :
                print("🛑 No active downloads. Closing session...")
                idm_status.close_session()

            idm_status.session_event.clear()  # Go back to waiting

def check_internet_connection(session,url):
    try:
        requests.get('https://www.google.com', timeout=5)
        return True
    except requests.ConnectionError:
        return False

async def retry_internet_check(session,url, max_retries=5, delay=1):

    for attempt in range(max_retries):
        # if check_internet_connection('https://www.google.com'):
        print("checking internet connection")
        if check_internet_connection(session, url):
            return True
        else:
            print(f"Attempt {attempt + 1}: No internet connection. Retrying in {delay} seconds...")
            await asyncio.sleep(delay)
    
    print("Max retries reached. Cancelling download.")
    return False

async def read_status_file():
    print("reading status file")
    try:
        async with asyncio.timeout(5):  # Timeout in 5 seconds
            async with idm_status.status_lock:
                print("getting token to read 😂 status file")
                save_state_file = os.path.join(SAVE_DIR,STATUS_DOWNLOAD_FILE)
                try:
                    async with aiofiles.open(save_state_file, mode='rb') as state_file:
                        bson_data = await state_file.read()
                        if bson_data:
                            idm_status.status_track = bson.loads(bson_data)
                except FileNotFoundError:
                    print(f"⚠️ Status File not found: {save_state_file}. Creating a new one...")
                    async with aiofiles.open(save_state_file, mode='wb') as new_file:
                        await new_file.write(bson.dumps({}))  # Create an empty BSON file
                    idm_status.status_track = {}
    except asyncio.TimeoutError:
        print("Possible deadlock. IN READING STATUS ⁉️")
        return False
   
async def write_status_file(new_status):
    print("writting status file")
    try:
        async with asyncio.timeout(5):  # Timeout in 5 seconds
            print(f"🧨status lock {idm_status.status_lock.locked}")
            async with idm_status.status_lock:
                print("getting token to write 😂 status file")
                async with aiofiles.open(SAVE_STATE_FILE, 'wb') as state_file:
                    bson_data = bson.dumps(new_status)
                    await state_file.write(bson_data)
                idm_status.status_track = new_status
            print("🤙 writting status with success")
            return True
    except asyncio.TimeoutError:
        print("Possible deadlock. IN WRITING NEW STATUS ⁉️")
        return False

# make idm_status.file_lock be the same for the same filename
async def write_chunk_to_file(tmp_path,file_path,File_Bytes,file_name,pos_start,total_size):
    if len(File_Bytes):
        async with idm_status.file_lock(file_name):
            if idm_status.status_track[file_name]:
                if not os.path.exists(tmp_path):
                    async with aiofiles.open(tmp_path, "wb") as f:
                        await f.write(b"")

                async with aiofiles.open(tmp_path, "r+b") as f:
                    await f.seek(pos_start)
                    await f.write(File_Bytes)

                # Rename to final_path when size matches
                if os.path.getsize(tmp_path) >= total_size:  # Check size
                    os.rename(tmp_path, file_path)  # Rename happens here

                await write_status_file(idm_status.status_track)

async def process_status_updates():
    print("🔄 process_status_updates() STARTED!")  # Debugging
    """Consumes the queue and updates idm_status by replacing old objects."""
    while True:
        print("🛠 Waiting for receiving status updates...")  # Debugging
        file_name, new_status_object = await idm_status.status_queue.get()  # Get the full object
        print(f"✅ Processing update: {file_name} -> new_status_object")
        async with idm_status.status_lock:
            if file_name:
                # updating the status of the file
                print("✅ ---got status_lock")
                idm_status.status_track[file_name]= new_status_object
                # print(f"✅ ----Updated {file_name}: {new_status_object}")
            elif new_status_object:
                newstatus={**idm_status.status_track,**new_status_object}
                # Creating a new merged dictionary
                idm_status.status_track= newstatus

        # add test if status_lock not changed
        await idm_status.socketio.emit('progres', idm_status.status_track)
        await write_status_file(idm_status.status_track)
        idm_status.status_queue.task_done()  # Mark task as done

def verify(file_infos):
    if not isinstance(file_infos, dict):
        raise ValueError("file_infos must be a dictionary")
    if not file_infos:
        raise ValueError("file_infos cannot be empty")