
from constants import STATUS_DOWNLOAD_FILE ,SAVE_DIR ,idm_status
import asyncio
import os

from observer_socket import get_socketio

from HandleDownload import download_file

from tool import read_status_file , write_status_file

async def stop_files(file_names=None,all=None):
    if not idm_status.socketio:
        idm_status.socketio=get_socketio()
    
    await read_status_file()

    if all:
        file_names = list(idm_status.status_track.keys())

    try:
        async with asyncio.timeout(5):   
            async with idm_status.status_lock:
                for file_name in file_names:
                    idm_status.status_track[file_name]['Status'] = False
                    print("😀send a stop signal to queue")
                    print("🛑stopped filed")
            await idm_status.status_queue.put((None, None))
        return True
    except asyncio.TimeoutError:
        print(" Possible deadlock. IN STOP_FILES ⁉️")
        return False

async def resume_files(file_names=None,all=None):

    if not idm_status.socketio:
        idm_status.socketio=get_socketio()

    await read_status_file()
    
    items = (
        [(file_name, "restart" if idm_status.status_track[file_name].get('Finished', False) else "continue")
         for file_name in idm_status.status_track.keys()] if all
        else file_names or []  # Default to empty list if file_names is None
    )

    for file_name, action in items: 
        item_downloading = idm_status.status_track.get(file_name, {}).get('Status', False)
        down_size = idm_status.status_track.get(file_name, {}).get('Downloaded', 0)
        filesize = idm_status.status_track.get(file_name, {}).get('File_Size', 0)
    
        if not item_downloading:
            print("resuming")
            down_size = idm_status.status_track.get(file_name, {}).get('Downloaded', 0)
            filesize = idm_status.status_track.get(file_name, {}).get('File_Size', 0)
            
            idm_status.status_track[file_name].update({
                'Status': True,
                'Finished': False,
                'Downloaded': 0 if down_size>=filesize  else down_size,
                'Cmd_Option': action
            })
            
            file_infos = idm_status.status_track[file_name]
            
            await download_file(file_infos)

async def delete_files(file_names=[],all=None):
    if not idm_status.socketio:
        idm_status.socketio=get_socketio()

    await read_status_file()

    if all:
        file_names = list(idm_status.status_track.keys())

    try:
        async with asyncio.timeout(5):   
            async with idm_status.status_lock:
                for file_name in file_names:
                    item=idm_status.status_track.get(file_name,{})
                    if item:
                        idm_status.status_track[file_name]['Status'] = False
                        del idm_status.status_track[file_name]

                    file_save_path = os.path.join( SAVE_DIR, file_name)
                    if os.path.exists(file_save_path) :
                        os.remove(file_save_path)

            await idm_status.status_queue.put((None, None))

        return True
    except asyncio.TimeoutError:
        print(" Possible deadlock. IN STOP_FILES ⁉️")
        return False