from Constants import STATUS_DOWNLOAD_FILE ,SAVE_DIR 
import Constants

import time
import asyncio
import requests
import bson
import os
import aiofiles

async def get_bandwith_speed(session, file_name,url, init_test_size=1024*1024):  # Test size 1MB
    
    global Constants

    Constants.status_tracker=read_status_file()

    headers = {'Range': f'bytes=0-{init_test_size-1}'}
    receivedData=0
    while Constants.status_tracker[file_name]['Status']:
        await asyncio.sleep(0.2)
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
                    print(test_size_bytes)
                    print(receivedData)
                    break  # Success, exit the loop
                except Exception as e:
                    factor+=1
                    # Reduce test_size_bytes if readexactly fails
                    test_size_bytes -= 1024  # Example reduction, adjust as needed
                    if test_size_bytes <= 1024:
                        Constants.status_tracker[file_name]['Speed']=test_size_bytes
                        break
                        # return test_size_bytes
                        # raise Exception("Failed to read any data")

            end_time = time.time()
            elapsed_time = end_time - start_time
            speed_in_bytes_per_second = receivedData / elapsed_time
            # print({"datasize":receivedData ,"time",elapsed_time})
            # Round the speed to 2 decimal places
            rounded_speed = round(speed_in_bytes_per_second)
            Constants.status_tracker[file_name]['Speed']=rounded_speed
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




def read_status_file():
    # global downloads
    save_state_file = os.path.join(SAVE_DIR,STATUS_DOWNLOAD_FILE)
    try:
        with open(save_state_file, mode='rb') as state_file:
            bson_data =state_file.read()
            downloads = bson.loads(bson_data)
            return downloads
    except FileNotFoundError:
        # Create an empty file if it doesn't exist
        initial_status = {}
        write_status_file(initial_status)
        return initial_status


async   def  write_status_file(new_status):
        save_state_file = os.path.join(SAVE_DIR,STATUS_DOWNLOAD_FILE)
        async with aiofiles.open(save_state_file, 'wb') as state_file:
            bson_data = bson.dumps(new_status)
            await state_file.write(bson_data)

    # with open(save_state_file, mode='wb') as state_file:
    #     bson_data = bson.dumps(new_status)
    #     state_file.write(bson_data)


async def write_chunk_to_file(file_path,File_Bytes,file_name,save_state_file):

    global Constants

    # print(downloads[file_name],"from writing to chunk")
    if Constants.status_tracker[file_name]:
        # print(f'appending {get_file_size(len(File_Bytes))}')
        with open(file_path, 'ab') as file:
            file.write(File_Bytes)
        # print("keeping track of file")
        async with aiofiles.open(save_state_file, 'wb') as state_file:
            bson_data = bson.dumps(Constants.status_tracker)
            await state_file.write(bson_data)
            # print("end writing")
    else:
        # Constants.status_tracker[file_name]
        pass
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

