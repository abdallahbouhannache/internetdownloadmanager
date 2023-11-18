import json
# from socket import SocketIO
from flask_socketio import SocketIO, emit
import aiohttp
import asyncio
import aiofiles

from tool import get_file_size
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import re
import requests
# from observer_socket import start_observer
import bson
# import observer_socket
from observer_socket import run_observer
import time

app = Flask(__name__)
# socketio = SocketIO(app)

# CORS(app,resources={r"/*":{"origins":"*"}})

# CORS(app)

downloads = {}

@app.route('/prepare_download_file', methods=['POST'])
async def download_header():
    print("grabbing file details")
    file_infos = request.get_json()
    file_url = file_infos.get('Url') or None
    save_dir = file_infos.get('SavePath') or "./"
    Catg=file_infos.get('Catg') or "UNKNOWN"
    speed_limit = file_infos.get('Speed') or None
    file_name = file_infos.get('FileName') or os.path.basename(file_url) 
    command = file_infos.get('Cmd_Option') or "new" # values continue,restart,new
    save_state_file = file_infos.get('download_state') or os.path.join(save_dir, 'download_state.bson')

    localDownload = {}
    downloaded_size=0
    random_id="0"

    # Get the filename from the response headers
    response = requests.get(file_url)
    file_size = len(response.content) or 0


    if not file_name :
        content_disposition = response.headers.get('Content-Disposition')
        file_name = get_filename_from_content_disposition(content_disposition)

    # Load the state from the save_state_file, if it exists
    if os.path.exists(save_state_file):
        async with aiofiles.open(save_state_file, mode='rb') as state_file:
            print('reading the file')
            bson_data =await state_file.read()
        # Decode BSON data
        localDownload = bson.loads(bson_data)

    file_save_path = os.path.join(save_dir, file_name)


    if os.path.exists(file_save_path) :

        if command=="restart":
            os.remove(file_save_path)

        elif command=="continue":
            downloaded_size=os.path.getsize(file_save_path)
            # if downloaded_size:
            #     localDownload[file_name]['Downloaded']=downloaded_size  
            # print("continue download of file_name from Downloaded ****")

        elif command=="new":
            import uuid
            random_id = uuid.uuid1()
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



    # building file entry in database
    localDownload[file_name] = {
    "id": random_id,
    "Url": file_url,
    "Status": True,
    "Downloaded": downloaded_size,
    "Cmd_Option": command,
    "Speed": speed_limit,
    "Catg":Catg,
    "FileName":file_name,
    "Time_Left": 0,
    "File_Size": file_size,
    "SavePath": save_dir,
    "Resume": False,
    }


    return jsonify(localDownload[file_name])
    # socketio.emit('filed', localDownload[file_name])



@app.route('/download_file', methods=['POST'])
async def download_file():
    # myresponse = app.make_response()
    # myresponse.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
    # myresponse.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
    # myresponse.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    print("starting download_file")
    file_infos = request.get_json()

    id = file_infos.get('id') or None
    if not id:
        file_infos=await download_header()
        id = file_infos.get('id')
        file_size = file_infos.get('File_Size')

    
    file_url = file_infos.get('Url') or None
    file_name = file_infos.get('FileName') or None
    Catg=file_infos.get('Catg') or "UNKNOWN"
    speed_limit = file_infos.get('Speed') or None
    downloaded_size = file_infos.get('Downloaded') or 0
    save_dir = file_infos.get('SavePath') or "./"
    command = file_infos.get('Cmd_Option') or "new" # values continue,restart,new
    save_state_file = os.path.join(save_dir, 'download_state.bson')
    file_save_path = os.path.join(save_dir, file_name)

    global downloads


    # # # URL of the file you want to download
    # # file_url = 'https://example.com/file_url'

    # # # Path where you want to save the downloaded file
    # # file_save_path = '/path/to/save/file.ext'

    # # # Speed limit in bytes per second
    # # speed_limit = 1024  # 1KB/s


    # # byte_range = 0
    # # # Load the start byte from the state file, if it exists
    # # if os.path.exists(save_state_file):
    # #     with open(save_state_file, 'r') as state_file:
    # #         state = json.load(state_file)
    # #     byte_range = int(state['Downloaded'])

    # # save_state_file = not save_state_file and os.path.join(save_dir, 'download_state.json')


    # # print({"filebrf":file_name})
    # # file_name = not file_name or os.path.basename(file_url) 
    

    # # Get the filename from the response headers
    # if not file_name :
    #     res = requests.get(file_url)
    #     content_disposition = res.headers.get('Content-Disposition')
    #     file_name = get_filename_from_content_disposition(content_disposition) 
    
    # size_of_file=0

    
    # # Load the state from the save_state_file, if it exists
    # if os.path.exists(save_state_file):

    #     async with aiofiles.open(save_state_file, mode='rb') as state_file:
    #         print('reading the file')
    #         bson_data =await state_file.read()

    #         # bson_data = bson.dumps(downloads)
    #         # await state_file.write(bson_data)
    #     # Read BSON data from a file
    #     # with open(save_state_file, 'rb') as file:
    #     #     bson_data = file.read()

    #     # Decode BSON data
    #     downloads = bson.loads(bson_data)
    #     # with open(save_state_file, 'r') as state_file:
    #     #         downloads = json.load(state_file)

    # file_save_path = os.path.join(save_dir, file_name)
    
    # # Create a unique state entry for each download
    # # if file_name not in downloads :
    # #     downloads[file_name] = {'Downloaded': 0, 'Status': True}

    # # downloads[file_name] = {'Downloaded': 0, 'Status': True}

    # if os.path.exists(file_save_path) :

    #     if command=="restart":
    #         os.remove(file_save_path)

    #     elif command=="continue":
    #         size_of_file=os.path.getsize(file_save_path)
    #         # if size_of_file:
    #         #     downloads[file_name]['Downloaded']=size_of_file  
    #         print("continue download of file_name from Downloaded ****")

    #     elif command=="new":
    #         # verify if not a continue|resume request ...
    #         [file_name,ext]=file_name.split('.')
    #         pattern = re.compile(f'^{re.escape(file_name)}(\(\d+\))?.{re.escape(ext)}$')
    #         content_dir=os.listdir(save_dir)
    #         # print(content_dir)
    #         # file_count=content_dir.count(pattern)
    #         matching_files = [f for f in content_dir if pattern.match(f)]
    #         file_count = len(matching_files)
    #         # print(file_name,ext)
    #         # print(f'file_count {file_count}')
    #         file_name=f'{file_name}({file_count+1}).{ext}'
    #         file_save_path = os.path.join(save_dir, file_name)






    # "last_byte": size_of_file,
    # "running": True,

    downloads[file_name] = {
    "id": "0",
    "Url": file_url,
    "Status": True,
    "Downloaded": downloaded_size,
    "Cmd_Option": command,
    "Speed": speed_limit,
    "Catg":Catg,
    "FileName":file_name,
    "Time_Left": 0,
    "File_Size": file_size,
    "SavePath": save_dir,
    "Resume": False,
    }

    # socketio.emit('filed', downloads[file_name])
    
    # if os.path.exists(file_save_path):
    #     if os.path.getsize(file_save_path):
    #         downloads[file_name]['Downloaded']=os.path.getsize(file_save_path)

    # print(downloads)

    # return 
    # headers = {'Range': 'bytes={}-'.format(byte_range)}
    # headers={'Range': f'bytes={byte_range}-{file_size}'}
    

    
    # Construct the headers using the byte range
    byte_range = downloads[file_name]['Downloaded']
    headers={'Range': f'bytes={byte_range}-'}
  

    async with aiohttp.ClientSession() as session:
        async with session.get(file_url,headers=headers) as response:
            # timer = time.time()

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

            # file_size = int(response.headers.get('Content-Length'))

            # Get the file size from the response headers
            file_size = int(response.headers.get('Content-Length', 0))
            if not downloads[file_name]['File_Size']==file_size:
                downloads[file_name]['File_Size']=file_size


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
                # if file_name in downloads and not downloads[file_name]['Status']:
                #     break
                # Check if the download has been stopped
                if not downloads[file_name]['Status']:
                    with aiofiles.open(save_state_file, mode='wb') as state_file:
                        print('Starting the file write')
                        bson_data = bson.dumps(downloads)
                        state_file.write(bson_data)
                        break

                    # with open(save_state_file, 'wb') as state_file:
                    #     # Convert JSON to BSON
                    #     bson_data = bson.dumps(downloads)
                    #     state_file.write(bson_data)
                    #     # state_file.write('\n')
                    #     # json.dump(downloads, state_file)
                    # break
                
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
                downloads[file_name]['Downloaded']=byte_range

                socketio.emit('progres', downloads)                
                print(f'downloading {byte_range}')

                # print(f'downloaded :--->{get_file_size(chunk_size)}')


                # Create a task to write the chunk to the file
                task = asyncio.create_task(write_chunk_to_file(file_save_path,data,file_name,save_state_file,file_size_on_disk))
                tasks.append(task)
                # print(f'All tasks completed in {time.time() - timer}s')


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
            # await asyncio.gather(*tasks)

    return f"File {file_name}  Download finish"


async def write_chunk_to_file(file_path, data, file_name,save_state_file,file_size_on_disk):
    print(f'appending {get_file_size(len(data))}')
    with open(file_path, 'ab') as file:
        file.write(data)
        
    #  # Save the current state to the save_state_file
    # with open(save_state_file, 'w') as state_file:
    #     json.dump(downloads, state_file)

   # Save the current state to the save_state_file

    if downloads[file_name]:
        print("keeping track of file")
        # with open(save_state_file, 'w') as state_file:
        #     json.dump(downloads, state_file)
        #     state_file.write('\n')
        #if file is added to downloads then update the state in the save_state_file
        async with aiofiles.open(save_state_file, 'wb') as state_file:
            bson_data = bson.dumps(downloads)
            await state_file.write(bson_data)

            # downloads[file_name]
    else:
        # here i do the creation of entry in the save_state_file to keep progress status
        # for persever progress data of downloads 
        pass 

    file_size_on_disk=os.path.getsize(file_path)
    # print(downloads,"before task started")

    response_data = downloads[file_name]
        # Return the response as JSON
    return jsonify(response_data)
   
    # return file_size_on_diskx

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
    return 'downloaded_file.html'

@app.route('/stop_download', methods=['POST'])
def stop_download():
    data = request.get_json()
    file_name = data.get('filename')
    returnStatus={file_name:file_name,"Status":False}

    if file_name in downloads:
        if downloads[file_name].get('Status'):
            downloads[file_name]['Status'] = False
            return f"Download of {file_name} stopped successfully"

    return f"the {file_name} is not running"

@app.route('/resume_download', methods=['POST'])
def resume_download():
    data = request.get_json()
    file_name = data.get('filename')

    if file_name in downloads:
        downloads[file_name]['Status'] = True
    else:
        downloads[file_name] = {'Status': True}

        # Start a new download task
        asyncio.create_task(download_file())

    return f"Download of {file_name} resumed"


# defining the flask app
def run_flask_app(socketio):
    print("FLASK & SOCKETS RUNNING OK ----->")
    socketio.run(app, debug=True,port=5001)
    # app.run(debug=True, port=5001)


if __name__ == '__main__':
    # loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(loop)

    socketio = SocketIO(app,cors_allowed_origins="*")
    
    # Run the Flask app and the observer in separate tasks

    # loop.create_task(run_observer(socketio))

    run_observer(socketio)
    run_flask_app(socketio)

    # loop.create_task(run_flask_app(socketio))

     # Run the event loop to keep the app running
    # loop.run_forever()

    # loop.run_until_complete(download_file())
    # start_observer(app)

    # observer_socket.run(app)
    
    # app.run(debug=True)
    # asyncio.run(download_file(),debug=True)
    # socketio.run(app)