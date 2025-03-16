# from constants import STATUS_DOWNLOAD_FILE ,SAVE_DIR, idm_status.status_track

from tool import get_bandwith_speed,write_chunk_to_file,retry_internet_check, read_status_file ,write_status_file
from flask import jsonify
import os
import re
import aiohttp
import asyncio
import aiofiles
import bson

from constants import STATUS_DOWNLOAD_FILE ,SAVE_DIR ,idm_status
from observer_socket import get_socketio,get_status
import requests
import tempfile

# global constants

async def download_file(file_infos):
    id = file_infos.get('id') or None
    file_url = file_infos.get('Url') or None
    file_name = file_infos.get('FileName') or None
    finished = file_infos.get('Finished') or False
    status = file_infos.get('Status') or False
    Catg=file_infos.get('Catg') or "UNKNOWN"
    # speed_limit = file_infos.get('Speed') or 2048
    speed_limit = 204800
    Conx_number = file_infos.get('Conx_number') or 2
    downloaded_size = file_infos.get('Downloaded') or 0
    save_dir = file_infos.get('SavePath') or "./downloads"
    command = file_infos.get('Cmd_Option') or "new" # values continue,restart,new
    save_state_file = os.path.join(SAVE_DIR, 'download_state.bson')
    file_save_path = os.path.join(save_dir, file_name)
    file_size = file_infos.get('File_Size') or 0

    # if os.path.exists(save_state_file):
    # await read_status_file()

    if os.path.exists(file_save_path) :
        downloaded_size=os.path.getsize(file_save_path)
        if command=="restart":
            os.remove(file_save_path)
            downloaded_size=0

    print("down_size",downloaded_size)
    print("filesize",file_size)
    print("resuming",0 if file_size==downloaded_size else downloaded_size)
    
    idm_status.status_track[file_name] = {
        "id": id,
        "Url": file_url,
        "Finished": finished,
        "Status": status,
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

    # socketio=get_socketio()
    # idm_status.socketio
    
    # add retry of grabbing file size here otherwise stop downloading
    # if not file_size:
    #     idm_status.status_track[file_name]['Status'] = False
        # await socketio.emit('progres', idm_status.status_track)
        # await write_status_file(idm_status.status_track)

    async with aiohttp.ClientSession() as session:
        internet=await retry_internet_check(session,"www.google.com")
        if not internet or not file_size:
            # await it here # add retry of grabbing file size here otherwise stop downloading
            idm_status.status_track[file_name]['Status'] = False
            await write_status_file(idm_status.status_track)
            await idm_status.socketio.emit('progres', idm_status.status_track)
            error="No internet connection" if not internet else f"File {file_name}  Filesize error"
            return jsonify({error}), 503
        print("internet and file_size is ok")

        try:
            await idm_status.socketio.emit('progres', idm_status.status_track)
            await write_status_file(idm_status.status_track)

            # Use tempfile for unique temp path
            with tempfile.NamedTemporaryFile(delete=False) as tmp:
                tmp_path = tmp.name
            print("-----------downloaded size pos-1",idm_status.status_track[file_name]['Downloaded'])
            tasks = []
            chunk_size = file_size // Conx_number # size of each chunk in bytes
            chunks = [(i * chunk_size, (i+1) * chunk_size - 1) for i in range(file_size // chunk_size)]
            for start, end in chunks:
                print(f"chunks: start={start}, end={end}")  
                print(f"chunks: some={start + end}")  
                task=download_task(session, file_url, start, end,file_name,file_save_path,tmp_path)
                tasks.append(task)
                await asyncio.sleep(0.1)

            # speed_task=get_bandwith_speed(session,file_name,file_url)
            # tasks.append(speed_task)

            print("getting started to download 1")
            await asyncio.gather(*tasks)
            print("finished the download tasks 1")            
        except ConnectionError as e:
            idm_status.status_track[file_name]['Status'] = False
            await write_status_file(idm_status.status_track)
            # socketio.emit('progres', idm_status.status_track)
            await idm_status.socketio.emit('progres', idm_status.status_track)
            print("error in fetching file")
            return jsonify({'error': 'Error starting download'}), 503
            # return

async def download_task(session, url, start, end,file_name,file_save_path,tmp_path):
    File_Bytes=bytearray()

    socketio=get_socketio()
    headers = {'Range': f'bytes={start}-{end}'}
    # headers = {'User-Agent': 'Mozilla/5.0'}
    
    # await read_status_file()
    async with session.get(url, headers=headers) as response:
        print("inside task x")
        async with idm_status.status_lock:
            local_file_status=idm_status.status_track.get(file_name, {})

        current_size = start      
        # await asyncio.sleep(0.1)
        while current_size <= end :
            print("inside loopo task x")
            await asyncio.sleep(1)
            async with idm_status.status_lock:  # Ensure safe read access
                file_status = idm_status.status_track.get(file_name, {}).get('Status', False)
                if not file_status:
                    print("file_status is false")
                    break
                speed = idm_status.status_track.get(file_name, {}).get('Speed', False)
                local_file_status['Speed']=speed

            try:
                remaining_bytes = end - current_size + 1
                chunk_size = min(speed, remaining_bytes)
                chunk = await asyncio.wait_for(response.content.read(chunk_size), timeout=5)
                if not chunk:
                    print("end of download")
                    break  # Exit loop if no more data
                File_Bytes+=chunk
                current_size += len(chunk)
                # socketio.emit('progres', idm_status.status_track)
                # idm_status.status_track[file_name]['Downloaded'] += len(chunk)
                local_file_status['Downloaded']+= len(chunk)
                await idm_status.status_queue.put((file_name, local_file_status))

                # updated_global_status = {**idm_status.status_track, **local_file_status}
                # await socketio.emit('progres', updated_global_status)

            except asyncio.TimeoutError:
                print(f"A connection error occurred: ")
                internet=await retry_internet_check(session,"www.google.com")
                if not internet:
                    # idm_status.status_track[file_name]['Status'] = False
                    local_file_status['Status']=False
                    break
                    # socketio.emit('progres', idm_status.status_track)
                    # socketio.emit('progres', idm_status.status_track)
                    # await write_status_file(idm_status.status_track)
                    # return jsonify({'error': 'No internet connection'}), 503
                # await asyncio.sleep(0.1)
                # continue
            except Exception as e:
                print('some other exception')
                # idm_status.status_track[file_name]['Status'] = False
                local_file_status['Status']=False
                break
                # socketio.emit('progres', idm_status.status_track)
                # return jsonify({'error': 'some error happened try later'}), 503


        # file_size=idm_status.status_track[file_name]['File_Size'] or 0
        file_size=local_file_status.get('File_Size') or 0
        downloaded_size=local_file_status.get('Downloaded') or 0

        print(f"downloading parts of [{file_name}]",local_file_status)
        if downloaded_size >= file_size :
            # idm_status.status_track[file_name]['Finished'] = True
            # idm_status.status_track[file_name]['Status'] = False
            local_file_status['Finished']=True
            local_file_status['Status']=False
            await idm_status.status_queue.put((file_name, local_file_status))

            # await socketio.emit('progres', updated_global_status)
            # await write_status_file(idm_status.status_track)

            print("download is finished  > ",local_file_status['Finished'])
            # socketio.emit('progres', idm_status.status_track)           

        

        await asyncio.sleep(0.5)
        await write_chunk_to_file(tmp_path,file_save_path,File_Bytes,file_name,start,file_size)

    print("finished task X")  


def get_file_name(FullFileName):
    # global constants 
    [file_name, ext] = FullFileName.rsplit(".",1) or [
        "download",
        "html",
      ]
    pattern = re.compile(f'^{re.escape(file_name)}(\\(\\d+\\))?\\.{re.escape(ext)}$')
    matching_files = [key for key in idm_status.status_track.keys() if pattern.match(key)]
    file_count = f'({len(matching_files)+1})' if len(matching_files) else ""

    unique_file_name=f'{file_name}{file_count}.{ext}'
    return unique_file_name,ext

def get_file_info(url, max_name_length=50):
    print("get_file_info")
    info = {
        'FileName': "download.html",
        'ext': "html",
        'File_Size': 0,
    }
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        # Try HEAD request first
        response = requests.head(url, headers=headers, allow_redirects=True, timeout=13)
        content_length = response.headers.get('Content-Length')
        print("HEAD response:", response.headers)

        # If Content-Length is missing, fall back to GET with stream
        if content_length is None:
            print("HEAD failed to get size, trying GET...")
            response = requests.get(url, stream=True, allow_redirects=True, timeout=13)
            content_length = response.headers.get('Content-Length')
            if content_length is None:
                print("Unable to retrieve file size from GET either.")
                return info  # Return default info if still no size

        file_size = int(content_length)
        filename = url.split("/")[-1] or "download"
        name, ext = get_file_name(filename)
        if len(name) > max_name_length:
            name = name[:max_name_length].rstrip()

        info = {
            'File_Size': file_size,
            'FileName': name,
            'ext': ext
        }
        return info

    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return info