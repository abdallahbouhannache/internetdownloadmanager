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

# global constants

async def download_file(file_infos):
    id = file_infos.get('id') or None
    file_url = file_infos.get('Url') or None
    file_name = file_infos.get('FileName') or None
    Catg=file_infos.get('Catg') or "UNKNOWN"
    speed_limit = file_infos.get('Speed') or 2048
    Conx_number = file_infos.get('Conx_number') or 2
    downloaded_size = file_infos.get('Downloaded') or 0
    save_dir = file_infos.get('SavePath') or "./downloads"
    command = file_infos.get('Cmd_Option') or "new" # values continue,restart,new
    save_state_file = os.path.join(SAVE_DIR, 'download_state.bson')
    file_save_path = os.path.join(save_dir, file_name)
    file_size = file_infos.get('File_Size') or 0

    if os.path.exists(save_state_file):
        idm_status.status_track= await read_status_file()

    if os.path.exists(file_save_path) :
        downloaded_size=os.path.getsize(file_save_path)
        if command=="restart":
            os.remove(file_save_path)

    idm_status.status_track[file_name] = {
    "id": id,
    "Url": file_url,
    "Finished": False,
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
    socketio=get_socketio()
    await write_status_file(idm_status.status_track)
    socketio.emit('progress', {file_name: idm_status.status_track[file_name]})

    if not file_size:
        return f"File {file_name}  Filesize error"

    internet=await retry_internet_check("")
    if not internet:
        idm_status.status_track[file_name]['Status'] = False
        await write_status_file(idm_status.status_track)
        socketio.emit('progress', {file_name: idm_status.status_track[file_name]})
        return jsonify({'error': 'No internet connection'}), 503
        # write_status_file(idm_status.status_track)
        # socketio.emit('progres', idm_status.status_track)
        # res="error in connection please try again in  a while"
        # return Response(res, status=503, mimetype='application/json')

    async with aiohttp.ClientSession() as session:
        try:
            tasks = []
            chunk_size = file_size // Conx_number # size of each chunk in bytes
            chunks = [(i * chunk_size, (i+1) * chunk_size - 1) for i in range(file_size // chunk_size)]            
            for start, end in chunks:
                
                task=download_task(session, file_url, start, end,file_name,file_save_path,save_state_file)
                tasks.append(task)
                
                await asyncio.sleep(0.1)

            speed_task=get_bandwith_speed(session,file_name,file_url)
            tasks.append(speed_task)

            await asyncio.gather(*tasks)
            
        except ConnectionError as e:
            idm_status.status_track[file_name]['Status'] = False
            await write_status_file(idm_status.status_track)
            # socketio.emit('progres', idm_status.status_track)
            socketio.emit('progress', {file_name: idm_status.status_track[file_name]})
            print("error in fetching file")
            return jsonify({'error': 'Error starting download'}), 503
            # return

async def download_task(session, url, start, end,file_name,file_save_path,save_state_file):
    # print("download_task being -------------")
    File_Bytes=bytearray()
    # global constants 
    socketio=get_socketio()
    #speed_limit=idm_status.status_track[file_name]['Speed']
    headers = {'Range': f'bytes={start}-{end}'}
    # timeout=60
    # print({"sped":sped})
    # print({"sped":speed_limit})
    idm_status.status_track= await read_status_file()
    async with session.get(url, headers=headers) as response:

        current_size = start
        file_size=idm_status.status_track[file_name]['File_Size']
        await asyncio.sleep(0.1)
        while current_size <= end and idm_status.status_track[file_name]['Status']:
            # print("from inside downloading")
            # print(idm_status.status_track[file_name]['Status'])
            downloaded_size=idm_status.status_track[file_name]['Downloaded']
            if downloaded_size >= file_size :
                idm_status.status_track[file_name]['Finished'] = True
                idm_status.status_track[file_name]['Status'] = False
                socketio.emit('progress', {file_name: idm_status.status_track[file_name]})
                break

            try:
                # speed=await get_bandwith_speed(session,file_name,url)
                speed=idm_status.status_track[file_name]['Speed']
                # speed=1024*1024
                # print({"speed",speed})
                # idm_status.status_track[file_name]['Speed']=speed
                # chunk = await response.content.readexactly(speed)
                chunk = await asyncio.wait_for(response.content.read(speed), timeout=1)
                # print(len(chunk))
                if not chunk:
                    print("end of download")
                    break  # Exit loop if no more data
                # print({"chunk",len(chunk)})
                # File_Bytes+=chunk
                File_Bytes=chunk
                current_size += len(chunk)
                idm_status.status_track[file_name]['Downloaded']=current_size
                socketio.emit('progres', idm_status.status_track)
            # except ConnectionError as e:
            except asyncio.TimeoutError:
                print(f"A connection error occurred: ")
                internet=await retry_internet_check("")
                if not internet:
                    idm_status.status_track[file_name]['Status'] = False
                    socketio.emit('progres', idm_status.status_track)
                    write_status_file(idm_status.status_track)
                    return jsonify({'error': 'No internet connection'}), 503
                continue
            except Exception as e:
                print('some other exception')
                idm_status.status_track[file_name]['Status'] = False
                socketio.emit('progres', idm_status.status_track)
                write_status_file(idm_status.status_track)
                return jsonify({'error': 'some error happened try later'}), 503


            # except Exception as e:
            #     internet=await retry_internet_check("")
            #     if not internet:
            #         idm_status.status_track[file_name]['Status'] = False
            #         socketio.emit('progres', idm_status.status_track)
            #         return jsonify({'error': 'No internet connection'}), 503
            #     print(f"An unexpected error occurred: {str(e)}")
            #     continue

            # data=await response.read()
            # print(idm_status.status_track)
            # EMIT EVERY 1SECOND
            # print(f'from --start:{start} downloading ---{get_file_size(downloaded_size)}--- filesize:{get_file_size(file_size)}: --end:{get_file_size(end)}')
            await asyncio.sleep(0.1)
            await write_chunk_to_file(file_save_path,File_Bytes,file_name,save_state_file)

        # print(f'fbytes {len(File_Bytes)}')
        # await write_chunk_to_file(file_save_path,File_Bytes,file_name,save_state_file)
        await asyncio.sleep(0.1)
        # response.release()



def get_file_name(FullFileName):

    # global constants 
    [file_name, ext] = FullFileName.rsplit(".",1) or [
        "download",
        "html",
      ]
    pattern = re.compile(f'^{re.escape(file_name)}(\\(\\d+\\))?\\.{re.escape(ext)}$')
    matching_files = [key for key in idm_status.status_track.keys() if pattern.match(key)]
    file_count = f'({len(matching_files)+1})' if len(matching_files) else ""

    # print("filecount",file_count)
    # print("filecount",idm_status.status_track)
    unique_file_name=f'{file_name}{file_count}.{ext}'
    return unique_file_name,ext


# def get_file_info(url,max_name_length=50):
#     print("get_file_info")

#     info = {
#         'FileName':"download.html",
#         'ext':"html",
#         'File_Size':0,
#         # 'status_code': response.status_code,
#         # 'content_length': response.headers.get('Content-Length'),
#         # 'content_type': response.headers.get('Content-Type'),
#         # 'last_modified': response.headers.get('Last-Modified')
#     }
#     try:
#         # Make a HEAD request to get file metadata quickly
#         response = requests.head(url, allow_redirects=True,timeout=13)
#         content_length = response.headers.get('Content-Length')
#         print("response",response)
#         # Extract and return relevant information
#         if content_length is None:
#             print("Unable to retrieve file size.")
#             return None, None
        
#         file_size = int(content_length)
#         # Extracting filename from URL
#         filename = url.split("/")[-1] or "download"  # Fallback if no filename
#         name, ext = get_file_name(filename)
#         # Truncate name if it exceeds max_name_length, preserving extension
#         if len(name) > max_name_length:
#             name = name[:max_name_length].rstrip()

#         info = {
#             'File_Size': file_size,
#             'FileName': name,
#             'ext': ext
#         }
        
#         return info
    
#     except requests.RequestException as e:
#         # Handle exceptions (e.g., network errors)
#         print(f"An error occurred: {e}")
#         return info



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


# Test
# url = "https://freetestdata.com/wp-content/uploads/2022/02/Free_Test_Data_15MB_MP4.mp4"
# result = get_file_info(url)
# print(result)