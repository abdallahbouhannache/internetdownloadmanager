
from constants import STATUS_DOWNLOAD_FILE ,SAVE_DIR ,idm_status
# import constants
import time
import asyncio
import requests
import bson
import os
import aiofiles

async def get_bandwith_speed(session, file_name,url, init_test_size=1024*1024,interval=0.2):  # Test size 1MB

    idm_status.status_track=await read_status_file()
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
                        # return test_size_bytes
                        # raise Exception("Failed to read any data")

            end_time = time.time()
            elapsed_time = end_time - start_time
            speed_in_bytes_per_second = receivedData / elapsed_time
            # print({"datasize":receivedData ,"time",elapsed_time})
            # Round the speed to 2 decimal places
            rounded_speed = round(speed_in_bytes_per_second)
            idm_status.status_track[file_name]['Speed']=rounded_speed
            # return rounded_speed


def check_internet_connection(url):
    try:
        requests.get('https://www.google.com', timeout=5)
        return True
    except requests.ConnectionError:
        return False


async def retry_internet_check(url, max_retries=5, delay=1):
    for attempt in range(max_retries):
        if check_internet_connection(url):
            return True
        else:
            print(f"Attempt {attempt + 1}: No internet connection. Retrying in {delay} seconds...")
            await asyncio.sleep(delay)
    else:
        print("Max retries reached. Cancelling download.")
        return False

async def read_status_file():
    print("reading status file")

    # idm_status.status_track={}
    save_state_file = os.path.join(SAVE_DIR,STATUS_DOWNLOAD_FILE)

    async with idm_status.status_lock:
        try:
            async with aiofiles.open(save_state_file, mode='rb') as state_file:
                bson_data = await state_file.read()
                if bson_data:
                    idm_status.status_track = bson.loads(bson_data)
                    # print("inside readstatus-----")
                    # print(idm_status.status_track)
                # return idm_status.status_track    
        except FileNotFoundError:
            # Create an empty file if it doesn't exist
            # initial_status = {}
            await write_status_file(idm_status.status_track)
            # return idm_status.status_track
        return idm_status.status_track


async   def  write_status_file(new_status):
    print("writting status file")
    async with idm_status.status_lock: 
        save_state_file = os.path.join(SAVE_DIR,STATUS_DOWNLOAD_FILE)
        async with aiofiles.open(save_state_file, 'wb') as state_file:
            bson_data = bson.dumps(new_status)
            await state_file.write(bson_data)

    # with open(save_state_file, mode='wb') as state_file:
    #     bson_data = bson.dumps(new_status)
    #     state_file.write(bson_data)


async def write_chunk_to_file(file_path,File_Bytes,file_name,save_state_file):
    # print(downloads[file_name],"from writing to chunk")
    print("writting chunks to downloaded file")
    print(idm_status.status_track)
    async with idm_status.file_lock: 
        if idm_status.status_track[file_name]:
            # print(f'appending {get_file_size(len(File_Bytes))}')
            with open(file_path, 'ab') as file:
                file.write(File_Bytes)
            # print("keeping track of file")
            async with aiofiles.open(save_state_file, 'wb') as state_file:
                bson_data = bson.dumps(idm_status.status_track)
                await state_file.write(bson_data)
                # print("end writing")
        # else:
            # idm_status.status_track[file_name]
            # pass
            # here i do the creation of entry in the save_state_file to keep progress status
            # for persever progress data of downloads 


# def get_file_size(content_length):

#     size = content_length
#     if(not isinstance(content_length,int)):
#         # Convert the content length to integer
#         size = int(content_length)

#     # Define the units
#     units = ['bytes', 'KB', 'MB']

#     # Iterate through the units and divide the size by 1024
#     for unit in units:
#         if size < 1024:
#             # Return the file size and unit
#             return f"{size:.2f} {unit}"
#         size /= 1024

#     # If the size is larger than the last unit, return in GB
#     return f"{size:.2f} GB"

