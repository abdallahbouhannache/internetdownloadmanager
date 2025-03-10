
from constants import STATUS_DOWNLOAD_FILE ,SAVE_DIR ,idm_status
# import constants
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
    # idm_status.status_track=get_status()
    idm_status.socketio=get_socketio()
    # print("idm_status.socketio",idm_status.socketio)
    # print("status_tracke before",idm_status.status_track)
    idm_status.status_track=await read_status_file()
    # print("idm_status.status_track",idm_status.status_track)
    

    if all:
        file_names = list(idm_status.status_track.keys())

    for file_name in file_names:
        idm_status.status_track[file_name]['Status'] = False
        idm_status.socketio.emit('progres', idm_status.status_track)
        # downloads[file_name]['Status']=False
        # Item=idm_status.status_track[file_name]['Status'] or True
        print("stopped filed")
        # if Item:
        #     idm_status.status_track[file_name]['Status'] = False

    time.sleep(0.05)
    await write_status_file(idm_status.status_track)

async def resume_files(file_names=None,all=None):
    idm_status.socketio=get_socketio()
    idm_status.status_track=await read_status_file()

    if all:
        file_names = list(idm_status.status_track.keys())

    for file_name in file_names:
        # Item=idm_status.status_track[file_name]['Status'] or False
        Item = idm_status.status_track.get(file_name, {}).get('Status', False)
        if not Item:
            print("resuming")
            idm_status.status_track[file_name]['Status'] = True
            file_infos = idm_status.status_track[file_name]
            # idm_status.socketio.emit('progres', idm_status.status_track)
            idm_status.socketio.emit('progress', {file_name: file_infos})
            await download_file(file_infos)

            # downloads[file_name]['Status']=True
            # asyncio.create_task(download_file(file_info))
            # asyncio.run(download_file(file_info))
            # lop = asyncio.get_event_loop()
            # lop.create_task(download_file(file_info))

    time.sleep(0.05)
    await write_status_file(idm_status.status_track)


async def delete_files(file_names=[],all=None):
    idm_status.socketio=get_socketio()
    idm_status.status_track=await read_status_file()

    if all:
        file_names = list(idm_status.status_track.keys())
    # print({"all":all})
    # print({"f":file_names})
    for file_name in file_names:
        Item=idm_status.status_track.get(file_name) or None
        if Item and Item.get('Status'):
            Item['Status'] = False
            # time.sleep(0.2)
        del idm_status.status_track[file_name]
        # print(idm_status.status_track)
        file_save_path = os.path.join( SAVE_DIR, file_name)
        if os.path.exists(file_save_path) :
            os.remove(file_save_path)

        print ("delete files ")
        print (idm_status.status_track)
        idm_status.socketio.emit('progres', {})

    await write_status_file(idm_status.status_track)