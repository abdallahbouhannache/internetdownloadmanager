from threading import Thread
from flask_socketio import SocketIO, emit
import aiohttp
import asyncio
import aiofiles
from tool import get_file_size
from Constants import STATUS_DOWNLOAD_FILE ,SAVE_DIR
from flask import Flask, request, jsonify ,Response
from flask_cors import CORS
import os
import re
import requests
import bson
from observer_socket import run_observer
import time

# from observer_socket import start_observer
# import observer_socket
# from socket import SocketIO
# from quart import Quart
# app = Quart(__name__)
# loop = asyncio.get_event_loop()
# socketio = SocketIO(app)
# CORS(app,resources={r"/*":{"origins":"*"}})
# CORS(app)

app = Flask(__name__)
socketio = SocketIO(app,cors_allowed_origins="*")
status_tracker = {}

@app.route('/get_file_name', methods=['GET'])
def get_file_name():
    file_infos = request.args.to_dict()
    file_name = file_infos.get('name') or 'dowload_file'
    ext = file_infos.get('ext') or "html"
    save_dir = file_infos.get('SavePath') or "./downloads"
    pattern = re.compile(f'^{re.escape(file_name)}(\(\d+\))?.{re.escape(ext)}$')
    content_dir=os.listdir(save_dir)
    matching_files = [f for f in content_dir if pattern.match(f)]
    file_count = f'({len(matching_files)})' if len(matching_files) else ""
    file_name=f'{file_name}{file_count}.{ext}'
    return file_name
    # print(len(matching_files))
    # print(file_count)


# @app.route('/prepare_download_file', methods=['POST'])
# async def download_header():

#     print("grabbing file details")
#     file_infos = request.get_json()
#     print(file_infos)

#     file_url = file_infos.get('Url') or None
#     save_dir = file_infos.get('SavePath') or "./"
#     Catg=file_infos.get('Catg') or "UNKNOWN"
#     speed_limit = file_infos.get('Speed') or None
#     file_name = file_infos.get('FileName') or os.path.basename(file_url) 
#     command = file_infos.get('Cmd_Option') or "new" # values continue,restart,new
#     save_state_file = os.path.join(save_dir, 'download_state.bson')
#     random_id = file_infos.get('id') or None

#     localDownload = {}
#     downloaded_size=0
#     if not random_id:
#         import uuid
#         random_id = uuid.uuid1()

#     response = requests.head(file_url)
#     file_size = int(response.headers.get('Content-Length', 0)) or 0
    
#     print("OVER HERE  !!!!!!")

#     if not file_name :
#         content_disposition = response.headers.get('Content-Disposition')
#         file_name = get_filename_from_content_disposition(content_disposition)

#     # Load the state from the save_state_file, if it exists
#     if os.path.exists(save_state_file):
#         with open(save_state_file, mode='rb') as state_file:
#             print('reading the file')
#             bson_data =state_file.read()
#         # Decode BSON data
#         localDownload = bson.loads(bson_data)
#     file_save_path = os.path.join(save_dir, file_name)


#     if localDownload.get(file_name):
#         if command=="restart":
#             os.remove(file_save_path)
#         elif command=="continue":
#             downloaded_size=os.path.getsize(file_save_path)
#             # if downloaded_size:
#             #     localDownload[file_name]['Downloaded']=downloaded_size  
#             # print("continue download of file_name from Downloaded ****")
#         elif command=="new":
#             # verify if not a continue|resume request ...
#             [file_name,ext]=file_name.split('.')
#             pattern = re.compile(f'^{re.escape(file_name)}(\(\d+\))?.{re.escape(ext)}$')
#             content_dir=os.listdir(save_dir)
#             # print(content_dir)
#             # file_count=content_dir.count(pattern)
#             matching_files = [f for f in content_dir if pattern.match(f)]
#             file_count = len(matching_files)
#             # print(file_name,ext)
#             # print(f'file_count {file_count}')
#             file_name=f'{file_name}({file_count+1}).{ext}'
#             file_save_path = os.path.join(save_dir, file_name)

#     # building file entry in database
#     localDownload[file_name] = {
#     "id": random_id,
#     "Url": file_url,
#     "Status": True,
#     "Downloaded": downloaded_size,
#     "Cmd_Option": command,
#     "Speed": speed_limit,
#     "Catg":Catg,
#     "FileName":file_name,
#     "Time_Left": 0,
#     "File_Size": file_size,
#     "SavePath": save_dir,
#     "Resume": False,
#     }

#     return jsonify(localDownload[file_name])
#     # socketio.emit('filed', localDownload[file_name])

async def download_file(file_infos):
    # print("starting download_file")
    id = file_infos.get('id') or None
    file_url = file_infos.get('Url') or None
    file_name = file_infos.get('FileName') or None
    Catg=file_infos.get('Catg') or "UNKNOWN"
    speed_limit = file_infos.get('Speed') or 2048
    Conx_number = file_infos.get('Conx_number') or 2

    # speed_limit = 80000
    downloaded_size = file_infos.get('Downloaded') or 0
    save_dir = file_infos.get('SavePath') or "./"
    command = file_infos.get('Cmd_Option') or "new" # values continue,restart,new
    save_state_file = os.path.join(save_dir, 'download_state.bson')
    file_save_path = os.path.join(save_dir, file_name)
    file_size = file_infos.get('File_Size') or 0

    global status_tracker

    if os.path.exists(save_state_file):
        with open(save_state_file, mode='rb') as state_file:
            # print('reading the file')
            bson_data =state_file.read()
        status_tracker = bson.loads(bson_data)

    file_save_path = os.path.join(save_dir, file_name)   

    if os.path.exists(file_save_path) :
        downloaded_size=os.path.getsize(file_save_path)
        if command=="restart":
            os.remove(file_save_path)

    status_tracker[file_name] = {
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
    
    async with aiofiles.open(save_state_file, 'wb') as state_file:
        bson_data = bson.dumps(status_tracker)
        await state_file.write(bson_data)


    if not file_size:
        return f"File {file_name}  Filesize error"

    internet=await retry_internet_check("")
    if not internet:
        status_tracker[file_name]['Status'] = False
        socketio.emit('progres', status_tracker)
        return jsonify({'error': 'No internet connection'}), 503
        # res="error in connection please try again in  a while"
        # return Response(res, status=503, mimetype='application/json')

    async with aiohttp.ClientSession() as session:
        try:
            tasks = []
            chunk_size = file_size // Conx_number # size of each chunk in bytes
            chunks = [(i * chunk_size, (i+1) * chunk_size - 1) for i in range(file_size // chunk_size)]
            
            for start, end in chunks:
                # print(start,end)
                task=download_task(session, file_url, start, end,file_name,file_save_path,save_state_file)
                tasks.append(task)
                # print(tasks)
                await asyncio.sleep(1)

            speed_task=get_bandwith_speed(session,file_name,file_url)
            tasks.append(speed_task)

            await asyncio.gather(*tasks)
            
        except ConnectionError as e:
            print("error in fetching file")
            # return

@app.route('/download_file', methods=['POST'])
async def download_file_api():
    file_infos = request.get_json()
    file_name = file_infos.get('name') or 'dowload_file'
    await download_file(file_infos)
    return f"File {file_name} Download finish"


async def get_bandwith_speed(session, file_name,url, init_test_size=1024*1024):  # Test size 1MB
    
    global status_tracker
    while status_tracker[file_name]['Status']:
        await asyncio.sleep(0.4)
        start_time = time.time()
        headers = {'Range': f'bytes=0-{init_test_size-1}'}
        receivedData=0
        factor=1
        async with session.get(url, headers=headers) as response:
            while True:
                try:
                    # Attempt to read exactly test_size_bytes
                    test_size_bytes = init_test_size
                    chunk = await response.content.read(test_size_bytes)
                    # chunk = await asyncio.wait_for(response.content.read(test_size_bytes), timeout=1)
                    receivedData=len(chunk)
                    break  # Success, exit the loop
                except EOFError:
                    factor+=1
                    # Reduce test_size_bytes if readexactly fails
                    test_size_bytes -= 1024*factor  # Example reduction, adjust as needed
                    if test_size_bytes <= 1024:
                        status_tracker[file_name]['Speed']=test_size_bytes
                        # return test_size_bytes
                        # raise Exception("Failed to read any data")

        end_time = time.time()
        elapsed_time = end_time - start_time
        speed_in_bytes_per_second = receivedData / elapsed_time
        # print({"datasize":receivedData ,"time",elapsed_time})
        # Round the speed to 2 decimal places
        rounded_speed = round(speed_in_bytes_per_second)
        status_tracker[file_name]['Speed']=rounded_speed
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





async def download_task(session, url, start, end,file_name,file_save_path,save_state_file):
    # print("download_task being -------------")
    File_Bytes=bytearray()
    global status_tracker
    
    # speed_limit=status_tracker[file_name]['Speed']

    headers = {'Range': f'bytes={start}-{end}'}
    # timeout=60

    # print({"sped":sped})
    # print({"sped":speed_limit})

    async with session.get(url, headers=headers) as response:
        # part_size = int(response.headers.get('Content-Length', 0))
        downloaded_size=status_tracker[file_name]['Downloaded']
        # downloaded_size += len(start)
        file_size=status_tracker[file_name]['File_Size']
        # print('\n')
        # print(f'start{start}')
        # print(f'end{end}')
        # print('\n')
        # print(f'dsize{downloaded_size}')
        # print(f'fsize{file_size}')
        # print(f'Partsize{part_size}')
        # print(status_tracker[file_name])
        # print('\n')
        await asyncio.sleep(1)
        # while downloaded_size < part_size :
        while downloaded_size < end and status_tracker[file_name]['Status']:
            # print("from inside downloading")
            # print(status_tracker[file_name]['Status'])
            try:
                # speed=await get_bandwith_speed(session,file_name,url)
                speed=status_tracker[file_name]['Speed']

                # speed=1024*1024
                # print({"speed",speed})
                # status_tracker[file_name]['Speed']=speed
                # chunk = await response.content.readexactly(speed)
                chunk = await asyncio.wait_for(response.content.read(speed), timeout=1)
                # print(len(chunk))
                if not chunk:
                    print("no chunk")
                    break  # Exit loop if no more data

                # print({"chunk",len(chunk)})
                # File_Bytes+=chunk
                File_Bytes=chunk
                downloaded_size += len(chunk)
                status_tracker[file_name]['Downloaded']=downloaded_size
                socketio.emit('progres', status_tracker)
            # except ConnectionError as e:
            except asyncio.TimeoutError:
                print(f"A connection error occurred: ")
                internet=await retry_internet_check("")
                if not internet:
                    status_tracker[file_name]['Status'] = False
                    socketio.emit('progres', status_tracker)
                    return jsonify({'error': 'No internet connection'}), 503
                continue
            except Exception as e:
                print('some other exception')
                break


            # except Exception as e:
            #     internet=await retry_internet_check("")
            #     if not internet:
            #         status_tracker[file_name]['Status'] = False
            #         socketio.emit('progres', status_tracker)
            #         return jsonify({'error': 'No internet connection'}), 503
            #     print(f"An unexpected error occurred: {str(e)}")
            #     continue

            # data=await response.read()
            # print(status_tracker)
            # EMIT EVERY 1SECOND
            # print(f'from --start:{start} downloading ---{get_file_size(downloaded_size)}--- filesize:{get_file_size(file_size)}: --end:{get_file_size(end)}')
            await asyncio.sleep(0.2)
            await write_chunk_to_file(file_save_path,File_Bytes,file_name,save_state_file)

        # print(f'fbytes {len(File_Bytes)}')
        # await write_chunk_to_file(file_save_path,File_Bytes,file_name,save_state_file)
        await asyncio.sleep(1)
        # response.release()

async def write_chunk_to_file(file_path,File_Bytes,file_name,save_state_file):

    global status_tracker
    # print(downloads[file_name],"from writing to chunk")
    if status_tracker[file_name]:
        # print(f'appending {get_file_size(len(File_Bytes))}')
        with open(file_path, 'ab') as file:
            file.write(File_Bytes)
        # print("keeping track of file")
        async with aiofiles.open(save_state_file, 'wb') as state_file:
            bson_data = bson.dumps(status_tracker)
            await state_file.write(bson_data)
            # print("end writing")
    else:
        # here i do the creation of entry in the save_state_file to keep progress status
        # for persever progress data of downloads 
        pass
  
def get_filename_from_content_disposition(content_disposition):
    if content_disposition:
        parts = content_disposition.split(';')
        for part in parts:
            if part.strip().startswith('filename='):
                filename = part.split('=')[1].strip().strip('"')
                return filename
    return 'downloaded_file.html'

def stop_files(file_names=None,all=None):
    # global downloads
    global status_tracker
    
    status_tracker=read_status_file()
    if all:
        file_names = list(status_tracker.keys())

    for file_name in file_names:
        status_tracker[file_name]['Status'] = False
        socketio.emit('progres', status_tracker)
        # downloads[file_name]['Status']=False
        # Item=status_tracker[file_name]['Status'] or True
        print("stopped filed")
        # if Item:
        #     status_tracker[file_name]['Status'] = False

    time.sleep(0.05)
    write_status_file(status_tracker)


@app.route('/stop_download', methods=['POST'])
def stop_download():
    data = request.get_json()
    all = data.get('all') or None
    save_state_file = os.path.join(SAVE_DIR,STATUS_DOWNLOAD_FILE)

    if not os.path.exists(save_state_file):
        print("error no file is on download")  
        return jsonify({"error":"error no file is on download"})
    else:
        if all:
            stop_files(all)
            res=f"All files are stopped"
        else:
            res=f"the selected files are stopped"
            items=data.get('rows') or None
            file_names=[item['FileName'] for item in items if 'FileName' in item]
            print("filename",file_names)
            stop_files(file_names)

    return Response(res, status=200, mimetype='application/json')
    # return f"the {file_name} is not running"

def resume_files(file_names=None,all=None):
    
    # global downloads
    global status_tracker

    status_tracker=read_status_file()
    if all:
        file_names = list(status_tracker.keys())

    for file_name in file_names:
        Item=status_tracker[file_name]['Status'] or False
        if not Item:
            print("resuming")
            status_tracker[file_name]['Status'] = True
            socketio.emit('progres', status_tracker)
            # downloads[file_name]['Status']=True
            file_info = status_tracker[file_name]
            asyncio.run(download_file(file_info))

            # lop = asyncio.get_event_loop()
            # lop.create_task(download_file(file_info))

    time.sleep(0.05)
    write_status_file(status_tracker)

@app.route('/resume_download', methods=['POST'])
def resume_download():
    data = request.get_json()
    all = data.get('all') or None
    save_state_file = os.path.join(SAVE_DIR,STATUS_DOWNLOAD_FILE)

    if not os.path.exists(save_state_file):
        res=f"error no file in download list"
    else:
        if all:
            resume_files(all)
            res=f"All files are resumed"
        else:
            res=f"the selected files are resumed"
            items=data.get('rows') or None
            file_names=[item['FileName'] for item in items if 'FileName' in item]
            print("filename_resume",file_names)
            resume_files(file_names)

    return Response(res, status=200, mimetype='application/json')


def read_status_file():
    # global downloads
    save_state_file = os.path.join(SAVE_DIR,STATUS_DOWNLOAD_FILE)
    with open(save_state_file, mode='rb') as state_file:
        bson_data =state_file.read()
        downloads = bson.loads(bson_data)
        return downloads

def  write_status_file(new_status):
    save_state_file = os.path.join(SAVE_DIR,STATUS_DOWNLOAD_FILE)
    with open(save_state_file, mode='wb') as state_file:
        bson_data = bson.dumps(new_status)
        state_file.write(bson_data)
    
def delete_files(file_names=None,all=None):

    status_tracker=read_status_file()
    if all:
        file_names = list(status_tracker.keys())

    # print({"all":all})
    # print({"f":file_names})
    for file_name in file_names:
        Item=status_tracker.get(file_name) or None
        if Item.get('Status'):
            Item['Status'] = False
            # time.sleep(0.2)
        del status_tracker[file_name]
        file_save_path = os.path.join( SAVE_DIR, file_name)
        if os.path.exists(file_save_path) :
            os.remove(file_save_path)
        socketio.emit('progres', status_tracker)

    write_status_file(status_tracker)
    
@app.route('/delete_download', methods=['POST'])
def delete_download():
    global status_tracker

    data = request.get_json()
    all = data.get('all') or None
    save_state_file = os.path.join(SAVE_DIR,STATUS_DOWNLOAD_FILE)

    if not os.path.exists(save_state_file):
        # print("error no file is on download")
        rs=f"error file status not found"
        # return Response(rs, status=200, mimetype='application/json')
    else:
        if all:
            delete_files(None,all)
            rs=f"the download list is emptied"
        else:
            items=data.get('rows') or None
            file_names=[item['FileName'] for item in items if 'FileName' in item]
            delete_files(file_names,None)
            rs=f"the selected files are deleted"
            
        # status_tracker=read_status_file()
        # print(status_tracker)
        # socketio.emit('progres', status_tracker)

    return Response(rs, status=200, mimetype='application/json')

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
    app.run(debug=True, port=5001)

if __name__ == '__main__':
    socketio_thread = Thread(target=run_observer(socketio))
    socketio_thread.start()
    run_flask_app(socketio)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)    
    run_observer(socketio)
     # Run the event loop to keep the app running
    loop.run_forever()
    