import json
import aiohttp
import asyncio
from tool import get_file_size
from flask import Flask, request, jsonify
import os
import re
import requests

app = Flask(__name__)

downloads = {}


@app.route('/download_file', methods=['POST'])
async def download_file():
    data = request.get_json()
    file_url = data.get('url') or None
    save_dir = data.get('path') or "./"
    file_name = data.get('filename') or None
    speed_limit = data.get('speed') or None
    command = data.get('command') or "new" # values continue,restart,new
    save_state_file = data.get('download_state') or os.path.join(save_dir, 'download_state.json')

    # # URL of the file you want to download
    # file_url = 'https://example.com/file_url'

    # # Path where you want to save the downloaded file
    # file_save_path = '/path/to/save/file.ext'

    # # Speed limit in bytes per second
    # speed_limit = 1024  # 1KB/s


    # byte_range = 0
    # # Load the start byte from the state file, if it exists
    # if os.path.exists(save_state_file):
    #     with open(save_state_file, 'r') as state_file:
    #         state = json.load(state_file)
    #     byte_range = int(state['last_byte'])

    # save_state_file = not save_state_file and os.path.join(save_dir, 'download_state.json')


    file_name = os.path.basename(file_url) if not file_name else "download"
    # Get the filename from the response headers
    if not file_name :
        res = requests.get(file_url)
        content_disposition = res.headers.get('Content-Disposition')
        file_name = get_filename_from_content_disposition(content_disposition)
    
    size_of_file=0

    global downloads
    # Load the state from the save_state_file, if it exists
    if os.path.exists(save_state_file):
        with open(save_state_file, 'r') as state_file:
                downloads = json.load(state_file) 

    file_save_path = os.path.join(save_dir, file_name)
    
    # Create a unique state entry for each download
    # if file_name not in downloads :
    #     downloads[file_name] = {'last_byte': 0, 'running': True}

    # downloads[file_name] = {'last_byte': 0, 'running': True}
    

    if os.path.exists(file_save_path) :

        if command=="restart":
            os.remove(file_save_path)

        elif command=="continue":
            size_of_file=os.path.getsize(file_save_path)
            # if size_of_file:
            #     downloads[file_name]['last_byte']=size_of_file  
            print("continue download of file_name from last_byte ****")

        elif command=="new":
            # verify if not a continue|resume request ...
            [file_name,ext]=file_name.split('.')
            pattern = re.compile(f'^{re.escape(file_name)}(\(\d+\))?.{re.escape(ext)}$')
            content_dir=os.listdir(save_dir)
            # print(content_dir)
            # file_count=content_dir.count(pattern)
            matching_files = [f for f in content_dir if pattern.match(f)]
            file_count = len(matching_files)
            # print(file_name,ext)
            # print(f'file_count {file_count}')
            file_name=f'{file_name}({file_count+1}).{ext}'
            file_save_path = os.path.join(save_dir, file_name)

    downloads[file_name] = {'last_byte': size_of_file, 'running': True}  

    # if os.path.exists(file_save_path):
    #     if os.path.getsize(file_save_path):
    #         downloads[file_name]['last_byte']=os.path.getsize(file_save_path)
    print(downloads)
    # return 

    byte_range = downloads[file_name]['last_byte']
    # Construct the headers using the byte range
    # headers = {'Range': 'bytes={}-'.format(byte_range)}

    headers={'Range': f'bytes={byte_range}-'}

    # headers={'Range': f'bytes={byte_range}-{file_size}'}
    
    print(downloads,"before task started")

    async with aiohttp.ClientSession() as session:
        async with session.get(file_url,headers=headers) as response:

            # file_name = os.path.basename(file_url) if not file_name else ""
            # # Get the filename from the response headers
            # if not file_name :
            #     content_disposition = response.headers.get('Content-Disposition')
            #     file_name = get_filename_from_content_disposition(content_disposition)

            # verify if not a continue|resume request ...
            # if not byte_range:
            #     [file_name,ext]=file_name.split('.')
            #     pattern = re.compile(f'^{re.escape(file_name)}(\(\d+\))?.{re.escape(ext)}$')
            #     content_dir=os.listdir(save_dir)
            #     # print(content_dir)
            #     # file_count=content_dir.count(pattern)
            #     matching_files = [f for f in content_dir if pattern.match(f)]
            #     file_count = len(matching_files)
            #     # print(file_name,ext)
            #     # print(f'file_count {file_count}')
            #     file_name=f'{file_name}({file_count+1}).{ext}'
            #     file_save_path = os.path.join(save_dir, file_name)


            # print(f'tobesaved_as_file_name={file_name}')
            # print(file_name)

            # Get the file size from the response headers
            # file_size = int(response.headers.get('Content-Length'))
            file_size = int(response.headers.get('Content-Length', 0))

            # print(get_file_size(file_size))
            # Calculate the number of chunks based on the speed limit
            # chunk_size = min(speed_limit, 1024*1024)
            chunk_size=500 * 1024 
            num_chunks = file_size // chunk_size
            # print(f'chunks {num_chunks} with chunk size  {get_file_size(chunk_size)} ')
            # Create a list to store the tasks for parallel downloading
            tasks = []
            file_size_on_disk = 0
            # Download the file in chunks asynchronously
            # for i in range(num_chunks):
            while file_size_on_disk < file_size :
                # # Check if the download has been stopped
                # if file_name in downloads and not downloads[file_name]['running']:
                #     break
                # Check if the download has been stopped
                if not downloads[file_name]['running']:
                    with open(save_state_file, 'w') as state_file:
                        json.dump(downloads, state_file)
                        state_file.write('\n')
                    break
                
                # Read a chunk of data from the response
                data = await response.content.read(256)

                # if not data:
                #     # Download is complete  
                #     downloads.pop(file_name)
                #     # if os.path.exists(save_state_file):
                #     #     os.remove(save_state_file)
                #     print("exited cause file downloading finish ,removed from download_state.json")
                #     break

                # Update the byte range
                byte_range += len(data)
                downloads[file_name]['last_byte']=byte_range

                # print(f'downloaded :--->{get_file_size(chunk_size)}')
                print(f'downloading {get_file_size(len(data))}')
                # Create a task to write the chunk to the file
                task = asyncio.create_task(write_chunk_to_file(file_save_path,data,file_name,save_state_file,file_size_on_disk))
                tasks.append(task)

                # task = asyncio.ensure_future(write_chunk_to_file(file_save_path,data))
                # task.add_done_callback(coroutine())
                # tasks.append(task)

                # Delay between chunks to limit the download speed
                await asyncio.sleep(1)
                # file_size_on_disk=os.path.getsize(file_save_path)

            # Download the remaining bytes
            # remaining_bytes = file_size % chunk_size
            # data = await response.content.read(remaining_bytes)
            # task = asyncio.create_task(write_chunk_to_file(file_save_path,data,file_name,save_state_file,file_size_on_disk))
            # tasks.append(task)

            # Wait for all tasks to complete
            await asyncio.gather(*tasks)

    return "File downloaded successfully"


async def write_chunk_to_file(file_path, data, file_name,save_state_file,file_size_on_disk):
    print(f'appending {get_file_size(len(data))}')
    with open(file_path, 'ab') as file:
        file.write(data)
    #  # Save the current state to the save_state_file
    # with open(save_state_file, 'w') as state_file:
    #     json.dump(downloads, state_file)
   # Save the current state to the save_state_file

    if downloads[file_name]:
        print("stored file")
        with open(save_state_file, 'w') as state_file:
            json.dump(downloads, state_file)
            state_file.write('\n')
            # downloads[file_name]

    file_size_on_disk=os.path.getsize(file_path)
    return file_size_on_disk


# def coroutine(file_path,file_name,save_state_file,file_size_on_disk):
#     with open(save_state_file, 'a') as state_file:
#         json.dump({file_name: downloads[file_name]}, state_file)
#         state_file.write('\n')
#     file_size_on_disk=os.path.getsize(file_path)
    

def get_filename_from_content_disposition(content_disposition):
    if content_disposition:
        parts = content_disposition.split(';')
        for part in parts:
            if part.strip().startswith('filename='):
                filename = part.split('=')[1].strip().strip('"')
                return filename
    return 'downloaded_file'


@app.route('/stop_download', methods=['POST'])
def stop_download():
    data = request.get_json()
    file_name = data.get('filename')
    returnStatus={file_name:file_name,"running":False}

    if file_name in downloads:
        if downloads[file_name].get('running'):
            downloads[file_name]['running'] = False
            return f"Download of {file_name} stopped successfully"

    return f"the {file_name} is not running"
        




@app.route('/resume_download', methods=['POST'])
def resume_download():
    data = request.get_json()
    file_name = data.get('filename')

    if file_name in downloads:
        downloads[file_name]['running'] = True
    else:
        downloads[file_name] = {'running': True}

        # Start a new download task
        asyncio.create_task(download_file())

    return f"Download of {file_name} resumed"



if __name__ == '__main__':
    app.run()
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(download_file())
    asyncio.run(download_file(),debug=True)