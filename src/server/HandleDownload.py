# from Constants import STATUS_DOWNLOAD_FILE ,SAVE_DIR, status_tracker

from tool import get_bandwith_speed,write_chunk_to_file,retry_internet_check, read_status_file ,write_status_file

import os
import aiohttp
import asyncio
import aiofiles
import bson

import Constants

from observer_socket import get_socketio,get_status



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
    save_dir = file_infos.get('SavePath') or "./downloads/"
    command = file_infos.get('Cmd_Option') or "new" # values continue,restart,new
    save_state_file = os.path.join(save_dir, 'download_state.bson')
    file_save_path = os.path.join(save_dir, file_name)
    file_size = file_infos.get('File_Size') or 0

    global Constants
    
    if os.path.exists(save_state_file):
        Constants.status_tracker=get_status()

        # with open(save_state_file, mode='rb') as state_file:
        #     # print('reading the file')
        #     bson_data =state_file.read()
        # Constants.status_tracker = bson.loads(bson_data)
    

    
    file_save_path = os.path.join(save_dir, file_name)   

    if os.path.exists(file_save_path) :
        downloaded_size=os.path.getsize(file_save_path)
        if command=="restart":
            os.remove(file_save_path)

    Constants.status_tracker[file_name] = {
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
        bson_data = bson.dumps(Constants.status_tracker)
        await state_file.write(bson_data)

    if not file_size:
        return f"File {file_name}  Filesize error"

    socketio=get_socketio()

    internet=await retry_internet_check("")
    if not internet:
        Constants.status_tracker[file_name]['Status'] = False
        write_status_file(Constants.status_tracker)
        socketio.emit('progres', Constants.status_tracker)
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
            Constants.status_tracker[file_name]['Status'] = False
            write_status_file(Constants.status_tracker)
        
            socketio.emit('progres', Constants.status_tracker)
            return jsonify({'error': 'Error starting download'}), 503
            print("error in fetching file")
            # return


async def download_task(session, url, start, end,file_name,file_save_path,save_state_file):
    # print("download_task being -------------")
    File_Bytes=bytearray()
    
    global Constants 

    socketio=get_socketio()
    
    # speed_limit=status_tracker[file_name]['Speed']

    headers = {'Range': f'bytes={start}-{end}'}
    # timeout=60

    # print({"sped":sped})
    # print({"sped":speed_limit})

    async with session.get(url, headers=headers) as response:
        # part_size = int(response.headers.get('Content-Length', 0))
        downloaded_size=Constants.status_tracker[file_name]['Downloaded']
        # downloaded_size += len(start)
        file_size=Constants.status_tracker[file_name]['File_Size']
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
        while downloaded_size < end and Constants.status_tracker[file_name]['Status']:
            # print("from inside downloading")
            # print(status_tracker[file_name]['Status'])
            try:
                # speed=await get_bandwith_speed(session,file_name,url)
                speed=Constants.status_tracker[file_name]['Speed']

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
                Constants.status_tracker[file_name]['Downloaded']=downloaded_size
                socketio.emit('progres', Constants.status_tracker)
            # except ConnectionError as e:
            except asyncio.TimeoutError:
                print(f"A connection error occurred: ")
                internet=await retry_internet_check("")
                if not internet:
                    Constants.status_tracker[file_name]['Status'] = False
                    socketio.emit('progres', Constants.status_tracker)
                    write_status_file(Constants.status_tracker)
                    return jsonify({'error': 'No internet connection'}), 503
                continue
            except Exception as e:
                print('some other exception')
                socketio.emit('progres', Constants.status_tracker)
                Constants.status_tracker[file_name]['Status'] = False
                write_status_file(Constants.status_tracker)
                return jsonify({'error': 'some error happened try later'}), 503
                


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

