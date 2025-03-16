
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
    if not idm_status.socketio:
        idm_status.socketio=get_socketio()   

    
    # await read_status_file()

    if all:
        file_names = list(idm_status.status_track.keys())

    try:
        async with asyncio.timeout(5):  # Timeout in 5 seconds   
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

    # print("resuming files working")
    # print(file_names)
    # print(idm_status.status_track.get('Free_Test_Data_15MB_MP4(2).mp4'))
    # print(type(idm_status.status_track))
    # return False
    # items = [(file_name, idm_status.status_track[file_name]) for file_name in idm_status.status_track.keys()]
    if not idm_status.socketio:
        idm_status.socketio=get_socketio()

    await read_status_file()

    
    # Prepare items based on 'all' condition
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
            # finished = idm_status.status_track.get('Finished', False)
            down_size = idm_status.status_track.get(file_name, {}).get('Downloaded', 0)
            filesize = idm_status.status_track.get(file_name, {}).get('File_Size', 0)
            
            idm_status.status_track[file_name].update({
                'Status': True,
                'Finished': False,
                'Downloaded': 0 if down_size>=filesize  else down_size,
                'Cmd_Option': action
            })
            
            file_infos = idm_status.status_track[file_name]

            # await idm_status.socketio.emit('progres', idm_status.status_track)

            await download_file(file_infos)

    await write_status_file(idm_status.status_track)

    # if all:
    #     file_names = list(idm_status.status_track.keys())
    #     for file_name in file_names:
    #         Item_Downloading = idm_status.status_track[file_name].get('Status', False)
    #         if not Item_Downloading:
    #             print("resuming")                
    #             finished = idm_status.status_track.get(file_name, {}).get('Finished', False)
    #             down_size = idm_status.status_track.get(file_name, {}).get('Downloaded', 0)
    #             idm_status.status_track[file_name].update({
    #                 'Status': True,
    #                 'Finished': False,
    #                 'Downloaded':0 if finished else down_size,
    #                 'Cmd_Option':  "restart" if finished else "continue"
    #             })
    #             file_infos = idm_status.status_track[file_name]
    #             idm_status.socketio.emit('progres', idm_status.status_track)
    #             await download_file(file_infos)
    # else:
    #     for file_name,action in file_names:
    #         Item_Downloading = idm_status.status_track.get(file_name, {}).get('Status', False)
    #         print("Item_Downloading",Item_Downloading)
    #         if not Item_Downloading:
    #             print("resuming")
    #             idm_status.status_track[file_name].update({
    #                 'Status': True,
    #                 'Finished': False,
    #                 'Downloaded':0,
    #                 'Cmd_Option': action
    #             })
    #             file_infos = idm_status.status_track[file_name]
    #             idm_status.socketio.emit('progres', idm_status.status_track)
    #             await download_file(file_infos)
            
    # await write_status_file(idm_status.status_track)


async def delete_files(file_names=[],all=None):
    idm_status.socketio=get_socketio()
    await read_status_file()

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
        await idm_status.socketio.emit('progres', {})

    await write_status_file(idm_status.status_track)