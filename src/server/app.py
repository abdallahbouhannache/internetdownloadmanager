import json
from threading import Thread

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

# from quart import Quart
# app = Quart(__name__)


# loop = asyncio.get_event_loop()
app = Flask(__name__)
socketio = SocketIO(app,cors_allowed_origins="*")
# socketio = SocketIO(app)

# CORS(app,resources={r"/*":{"origins":"*"}})

# CORS(app)

downloads = {}


# def get_file_details(url):
#     parsed_url = urlparse(url)
#     path = parsed_url.path
#     filename = Path(path).name
#     filename_without_extension = Path(filename).stem
#     file_extension = Path(filename).suffix
#     return filename, filename_without_extension, file_extension

# def get_file_size(url):
#    response = requests.head(url)
#    file_size = int(response.headers.get('Content-Length', 0))
#    return file_size


@app.route('/get_file_name', methods=['GET'])
def get_file_name():
    file_infos = request.args.to_dict()
    file_name = file_infos.get('name') or 'dowload_file'
    ext = file_infos.get('ext') or "html"
    save_dir = file_infos.get('SavePath') or "./"
    pattern = re.compile(f'^{re.escape(file_name)}(\(\d+\))?.{re.escape(ext)}$')
    content_dir=os.listdir(save_dir)
    matching_files = [f for f in content_dir if pattern.match(f)]
    # print(len(matching_files))
    file_count = f'({len(matching_files)})' if len(matching_files) else ""
    print(file_count)
    file_name=f'{file_name}{file_count}.{ext}'

    # print(file_infos)
    # print(file_count)
    # print(file_name)
    # file_infos = request.get_json()
    # file_infos = request.args
    # [file_name,ext]=file_infos.split('.')
    # print(content_dir)
    # file_count=content_dir.count(pattern)
    # print(file_name,ext)
    # print(f'file_count {file_count}')    

    return file_name



@app.route('/prepare_download_file', methods=['POST'])
async def download_header():

    print("grabbing file details")
    file_infos = request.get_json()
    print(file_infos)

    file_url = file_infos.get('Url') or None
    save_dir = file_infos.get('SavePath') or "./"
    Catg=file_infos.get('Catg') or "UNKNOWN"
    speed_limit = file_infos.get('Speed') or None
    file_name = file_infos.get('FileName') or os.path.basename(file_url) 
    command = file_infos.get('Cmd_Option') or "new" # values continue,restart,new
    save_state_file = os.path.join(save_dir, 'download_state.bson')
    random_id = file_infos.get('id') or None

    localDownload = {}
    downloaded_size=0
    if not random_id:
        import uuid
        random_id = uuid.uuid1()


    # Get the filename from the response headers
    # response = requests.get(file_url)

    response = requests.head(file_url)
    file_size = int(response.headers.get('Content-Length', 0)) or 0
    # file_size = len(response.content) or 0
    
    # file_size =  0

    print("OVER HERE  !!!!!!")

    if not file_name :
        content_disposition = response.headers.get('Content-Disposition')
        file_name = get_filename_from_content_disposition(content_disposition)

    # Load the state from the save_state_file, if it exists
    if os.path.exists(save_state_file):
        with open(save_state_file, mode='rb') as state_file:
            print('reading the file')
            bson_data =state_file.read()
        # Decode BSON data
        localDownload = bson.loads(bson_data)
    file_save_path = os.path.join(save_dir, file_name)


    if localDownload.get(file_name):
        if command=="restart":
            os.remove(file_save_path)
        elif command=="continue":
            downloaded_size=os.path.getsize(file_save_path)
            # if downloaded_size:
            #     localDownload[file_name]['Downloaded']=downloaded_size  
            # print("continue download of file_name from Downloaded ****")
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
    print("starting download_file")
    file_infos = request.get_json()
    id = file_infos.get('id') or None
    file_url = file_infos.get('Url') or None
    file_name = file_infos.get('FileName') or None
    Catg=file_infos.get('Catg') or "UNKNOWN"
    speed_limit = file_infos.get('Speed') or 2048
    Conx_number = file_infos.get('Conx_number') or 2

    speed_limit = 80000
    downloaded_size = file_infos.get('Downloaded') or 0
    save_dir = file_infos.get('SavePath') or "./"
    command = file_infos.get('Cmd_Option') or "new" # values continue,restart,new
    save_state_file = os.path.join(save_dir, 'download_state.bson')
    file_save_path = os.path.join(save_dir, file_name)
    file_size = file_infos.get('File_Size') or 0


    global downloads

    if os.path.exists(save_state_file):
        with open(save_state_file, mode='rb') as state_file:
            print('reading the file')
            bson_data =state_file.read()

        downloads = bson.loads(bson_data)

    file_save_path = os.path.join(save_dir, file_name)   

    if os.path.exists(file_save_path) :
        downloaded_size=os.path.getsize(file_save_path)
        if command=="restart":
            os.remove(file_save_path)

    downloads[file_name] = {
    "id": id,
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

    
    # File_Bytes=bytearray()
    


    # byte_range = downloads[file_name]['Downloaded']
    # headers={'Range': f'bytes={byte_range}-'}
    # Get the current event loop    
    # session = aiohttp.ClientSession(limits=aiohttp.Limits(
    #max_connections=5 # limit to 5 concurrent connections
    # )
    # )
    async with aiohttp.ClientSession() as session:
        # async with session.get(file_url,headers=headers) as response:

        # file_size = int(response.headers.get('Content-Length', 0))
        # if not downloads[file_name]['File_Size']==file_size:
        #     downloads[file_name]['File_Size']=file_size

        # chunk_size=500 * 1024 
        # num_chunks = file_size // chunk_size

        

        tasks = []

        # connexions=Conx_number

        # file_size = 1000000 # size of the file in bytes
        chunk_size = file_size // Conx_number # size of each chunk in bytes

        chunks = [(i * chunk_size, (i+1) * chunk_size - 1) for i in range(file_size // chunk_size)]

        # while downloaded_size < file_size :

        # for cnx in range(0,connexions):
        for start, end in chunks:
            print(start,end)
            # task = await asyncio.create_task(my_task())
            # task = await asyncio.create_task(download_task(session, file_url, start, end,file_name,downloads,file_save_path,save_state_file))
            task=download_task(session, file_url, start, end,file_name,file_save_path,save_state_file)
            tasks.append(task)
            print(tasks)
            await asyncio.sleep(1)

        await asyncio.gather(*tasks)
        
        # print(downloads)
        # print(len(File_Bytes))

        # await write_chunk_to_file(file_save_path,File_Bytes,downloads,file_name,save_state_file)

    return f"File {file_name}  Download finish"



async def download_task(session, url, start, end,file_name,file_save_path,save_state_file):
    print("download_task being -------------")
    
    File_Bytes=bytearray()

    if not downloads[file_name]['Status']:
        with open(save_state_file, mode='wb') as state_file:
            print('Starting the file write')
            bson_data = bson.dumps(downloads)
            state_file.write(bson_data)
            # return None

    speed_limit=downloads[file_name]['Speed']
    headers = {'Range': f'bytes={start}-{end}'}

    async with session.get(url, headers=headers) as response:
        part_size = int(response.headers.get('Content-Length', 0))
        # downloaded_size=os.path.getsize(file_path)
        # downloaded_size=downloads[file_name]['Downloaded']
        downloaded_size=start
        file_size=downloads[file_name]['File_Size']
        print('\n')

        print(f'start{start}')
        print(f'end{end}')
        print('\n')

        print(f'dsize{downloaded_size}')
        print(f'fsize{file_size}')
        print(f'Partsize{part_size}')
        print(downloads[file_name])
        print('\n')
        await asyncio.sleep(1)
        
        # while downloaded_size < part_size :
        while downloaded_size < end :
            try:
                chunk = await response.content.read(speed_limit)
                File_Bytes+=chunk
                downloaded_size += len(chunk)
                downloads[file_name]['Downloaded']=downloaded_size
                socketio.emit('progres', downloads)
            except ConnectionError as e:
                print(f"A connection error occurred: {str(e)}")
                continue
            except Exception as e:
                print(f"An unexpected error occurred: {str(e)}")
                continue
            # data=await response.read()
            # print(downloads)
            # EMIT EVERY 1SECOND
            
            print(f'from --start:{start} downloading ---{downloaded_size}--- filesize:{file_size}: --end:{end}')
            await asyncio.sleep(1)

        print(f'fbytes {len(File_Bytes)}')

        await write_chunk_to_file(file_save_path,File_Bytes,file_name,save_state_file)
        await asyncio.sleep(1)

        # response.release()

async def write_chunk_to_file(file_path,File_Bytes,file_name,save_state_file):

    #  # Save the current state to the save_state_file
    # with open(save_state_file, 'w') as state_file:
    #     json.dump(downloads, state_file)
   # Save the current state to the save_state_file
    print(downloads[file_name],"from writing to chunk")

    if downloads[file_name]:
        print(f'appending {get_file_size(len(File_Bytes))}')
        with open(file_path, 'ab') as file:
            file.write(File_Bytes)
        print("keeping track of file")
        # with open(save_state_file, 'w') as state_file:
        #     json.dump(downloads, state_file)
        #     state_file.write('\n')
        #if file is added to downloads then update the state in the save_state_file
        async with aiofiles.open(save_state_file, 'wb') as state_file:
            bson_data = bson.dumps(downloads)
            await state_file.write(bson_data)
            print("end writing")
            # downloads[file_name]
    else:
        # here i do the creation of entry in the save_state_file to keep progress status
        # for persever progress data of downloads 
        pass 

    # file_size_on_disk=os.path.getsize(file_path)
    
    # print(downloads,"before task started")

    response_data = downloads[file_name]
    # Return the response as JSON
    # return jsonify(response_data)
   
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


@app.route('/resume', methods=['GET'])
def handle_my_custom_event():
 loop = asyncio.get_event_loop()
 loop.create_task(async_task())
#  socketio.start_background_task(async_task)
 print('asyncio called1')
 return "asyncio called1"


async def async_task():
 print("asyncio completed")
 await asyncio.sleep(1)
 return "asyncio completed"

# defining the flask app
def run_flask_app(socketio):
    print("FLASK & SOCKETS RUNNING OK ----->")
    # loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(loop)
    # loop = asyncio.get_event_loop()

    # print("loop----------")
    # print(loop)

    # socketio.run(app, debug=True,port=5001)
    app.run(debug=True, port=5001)


if __name__ == '__main__':
    
    # run_observer(socketio)
    # Start the Flask-SocketIO server in a separate thread
    socketio_thread = Thread(target=run_observer(socketio))
    socketio_thread.start()
    run_flask_app(socketio)
    # run_flask_app(socketio)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)    
    # Run the Flask app and the observer in separate tasks
    # run_observer(socketio)
    # loop.run_until_complete(run_observer(socketio))
    run_observer(socketio)
     # Run the event loop to keep the app running
    loop.run_forever()
    # loop.run_until_complete(download_file())
    # start_observer(app)
    # observer_socket.run(app)
    # app.run(debug=True)
    # asyncio.run(download_file(),debug=True)
    # socketio.run(app)