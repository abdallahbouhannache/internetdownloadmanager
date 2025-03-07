from Constants import STATUS_DOWNLOAD_FILE ,SAVE_DIR 
import Constants
import time
import asyncio
import os

from observer_socket import get_socketio

from HandleDownload import download_file

from tool import read_status_file , write_status_file
  
# def get_filename_from_content_disposition(content_disposition):
#     if content_disposition:
#         parts = content_disposition.split(';')
#         for part in parts:
#             if part.strip().startswith('filename='):
#                 filename = part.split('=')[1].strip().strip('"')
#                 return filename
#     return 'downloaded_file.html'

async def stop_files(file_names=None,all=None):
    # global downloads
    global Constants
    
    # Constants.status_tracker=get_status()
    socketio=get_socketio()
    # print("socketio",socketio)

    # print("status_tracke before",Constants.status_tracker)
    Constants.status_tracker=await read_status_file()
    # print("status_tracker",Constants.status_tracker)
    

    if all:
        file_names = list(Constants.status_tracker.keys())

    for file_name in file_names:
        Constants.status_tracker[file_name]['Status'] = False
        socketio.emit('progres', Constants.status_tracker)
        # downloads[file_name]['Status']=False
        # Item=status_tracker[file_name]['Status'] or True
        print("stopped filed")
        # if Item:
        #     status_tracker[file_name]['Status'] = False

    time.sleep(0.05)
    await write_status_file(Constants.status_tracker)

async def resume_files(file_names=None,all=None):
    # global downloads
    global Constants

    socketio=get_socketio()
    Constants.status_tracker=await read_status_file()

    if all:
        file_names = list(Constants.status_tracker.keys())

    for file_name in file_names:
        Item=Constants.status_tracker[file_name]['Status'] or False
        if not Item:
            print("resuming")
            Constants.status_tracker[file_name]['Status'] = True
            socketio.emit('progres', Constants.status_tracker)
            # downloads[file_name]['Status']=True
            file_infos = Constants.status_tracker[file_name]
            await download_file(file_infos)

            # asyncio.create_task(download_file(file_info))
            # asyncio.run(download_file(file_info))
            # lop = asyncio.get_event_loop()
            # lop.create_task(download_file(file_info))

    time.sleep(0.05)
    await write_status_file(Constants.status_tracker)


async def delete_files(file_names=[],all=None):

    global Constants

    socketio=get_socketio()
    Constants.status_tracker=await read_status_file()

    if all:
        file_names = list(Constants.status_tracker.keys())

    # print({"all":all})
    # print({"f":file_names})
    for file_name in file_names:
        Item=Constants.status_tracker.get(file_name) or None
        if Item and Item.get('Status'):
            Item['Status'] = False
            # time.sleep(0.2)
        del Constants.status_tracker[file_name]
        # print(Constants.status_tracker)
        file_save_path = os.path.join( SAVE_DIR, file_name)
        if os.path.exists(file_save_path) :
            os.remove(file_save_path)
        socketio.emit('progres', Constants.status_tracker)

    await write_status_file(Constants.status_tracker)