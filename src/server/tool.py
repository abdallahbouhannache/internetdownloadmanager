
import aiohttp
from constants import STATUS_DOWNLOAD_FILE ,SAVE_DIR ,idm_status,SAVE_STATE_FILE
# import constants
import time
import asyncio
import requests
import bson
import os
import aiofiles


async def process_status_updates():
    print("🔄 process_status_updates() STARTED!")  # Debugging

    """Consumes the queue and updates idm_status by replacing old objects."""
    while True:
        print("🛠 Waiting for status updates...")  # Debugging
        file_name, new_status_object = await idm_status.status_queue.get()  # Get the full object
        print(f"✅ Processing update: {file_name} -> new_status_object")
        async with idm_status.status_lock:
            if file_name:
                # updating the status of the file
                print("✅ ---got status_lock")
                idm_status.status_track[file_name]= new_status_object
                print(f"✅ ----Updated {file_name}: {new_status_object}")
            elif new_status_object:
                newstatus={**idm_status.status_track,**new_status_object}
                # Creating a new merged dictionary
                idm_status.status_track= newstatus
                # Replace the whole status object
                # idm_status.status_track= new_status_object

        await idm_status.socketio.emit('progres', idm_status.status_track)
        await write_status_file(idm_status.status_track)
        idm_status.status_queue.task_done()  # Mark task as done

async def get_bandwith_speed(session, file_name,url, init_test_size=1024*1024,interval=0.2):  # Test size 1MB
    # await read_status_file()
    headers = {'Range': f'bytes=0-{init_test_size-1}'}
    receivedData=0
    rounded_speed=0
    while idm_status.status_track[file_name]['Status']:
        if abs(rounded_speed) > 300000:
            interval = min(interval + 0.1, 2.0)
        else:
            interval = max(interval - 0.1, 0.1)
        await asyncio.sleep(interval)
        start_time = time.time()
        factor=1
        test_size_bytes = init_test_size
        async with session.get(url, headers=headers) as response:
            while True:
                try:
                    # Attempt to read exactly test_size_bytes
                    chunk = await response.content.readexactly(test_size_bytes)
                    # chunk = await asyncio.wait_for(response.content.readexactly(test_size_bytes), timeout=1)
                    receivedData=len(chunk)
                    # print(test_size_bytes)
                    # print(receivedData)
                    break  # Success, exit the loop
                except Exception as e:
                    factor+=1
                    # Reduce test_size_bytes if readexactly fails
                    test_size_bytes -= 1024  # Example reduction, adjust as needed
                    if test_size_bytes <= 1024:
                        idm_status.status_track[file_name]['Speed']=10000
                        break

            end_time = time.time()
            elapsed_time = end_time - start_time
            speed_in_bytes_per_second = receivedData / elapsed_time
            rounded_speed = round(speed_in_bytes_per_second)
            idm_status.status_track[file_name]['Speed']=rounded_speed
            # return rounded_speed
    print("finished bandwidth")


def check_internet_connection(session,url):
    try:
        requests.get('https://www.google.com', timeout=5)
        return True
    except requests.ConnectionError:
        return False

# async def check_internet_connection(session, url):
#     try:retry_internet_check
#         async with session.get(url, timeout=aiohttp.ClientTimeout(total=100)) as response:
#             return True
#     except (aiohttp.ClientError, asyncio.TimeoutError):
#         return False

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
    # if not idm_status._status_file_loaded:
    #     idm_status._status_file_loaded=True
    #     return False
    
    # idm_status.status_track={}
    # if os.path.exists(save_state_file):
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

# make changes for idm_status.file_lock so it can all files write concurrently
async def write_chunk_to_file(tmp_path,file_path,File_Bytes,file_name,pos_start,total_size):
    if len(File_Bytes):
        # print("writting chunks to downloaded file")
        # print(f"chunk length {len(File_Bytes)}")
        async with idm_status.file_lock: 
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

def verify(file_infos):
    if not isinstance(file_infos, dict):
        raise ValueError("file_infos must be a dictionary")
    if not file_infos:
        raise ValueError("file_infos cannot be empty")
