
import os
import aiofiles
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
# from watchdog.observers import Observer
# from watchdog.events import FileSystemEventHandler
import jsonpatch
import bson

from tool import read_status_file ,process_status_updates

from constants import STATUS_DOWNLOAD_FILE ,SAVE_DIR ,idm_status,SAVE_STATE_FILE

import asyncio

import socketio

# import constants

# from flask_cors import CORS
# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'your-secret-key'
# CORS(app,resources={r"/*":{"origins":"*"}})


# SAVE_STATE_FILE = os.path.join(SAVE_DIR, STATUS_DOWNLOAD_FILE)




# class FileChangeHandler(FileSystemEventHandler):
#     def __init__(self, socketio,loop):
#         self.socketio = socketio
#         self.loop = loop

#     def on_modified(self, event):
#         if not event.is_directory and event.src_path == SAVE_STATE_FILE:
#             print('modified DETECTION bef handle')
#             asyncio.run_coroutine_threadsafe(self.handle_modified(event.src_path), self.loop)

#     async def handle_modified(self, file_path):
#         print('handle_modified CALLED')
#         async with aiofiles.open(file_path, mode='rb') as state_file:
#             print('SENDING CHANGES TOWARD FRONT')
#             bson_data = await state_file.read()
#             downloads_state = bson.loads(bson_data)
#             self.socketio.emit('progres', downloads_state)


# start_observer(socketio)
# idm_status.status_track=await read_status_file()
# emit('load', idm_status.status_track)
 # if os.path.exists(SAVE_STATE_FILE):
        #     with open(SAVE_STATE_FILE, 'rb') as file:
        #         bson_data = file.read()                
        #         if bson_data:
        #             idm_status.status_track = bson.loads(bson_data)
        #         # emit('load', idm_status.status_track)

                # idm_status.socketio.emit('load', idm_status.status_track)

                # print(f"downloads_state:{downloads_state}")

def start_observer(socketio):
    @socketio.on('connect')
    async def handle_connect(sid, environ):

        if not idm_status._status_file_loaded:
            idm_status._status_file_loaded=True
            await read_status_file()

        

        await socketio.emit('load', idm_status.status_track, room=sid)

       
        print('socket backend : Client connected')

    @socketio.on('disconnect')
    async def handle_disconnect(sid):
        # observer.stop()
        # observer.join()
        print('socket backend :Client disconnected')

    # @socketio.on('progres')
    # def handle_progres(data):
    #     print('socket backend :sending you files status ', data)
        # with open("./download_state.bson", 'rb') as file:
        #     bson_data = file.read()
        #     # Decode BSON data
        #     downloads_state = bson.loads(bson_data)
        #     socketio.emit('progres', downloads_state)
        # socketio.emit('progres', {"dat":'yes progres am here:sent from backend'})

    @socketio.on('message')
    async def handle_message(msg):
        print('socket backend : Received message ', msg)
        await  socketio.emit('message', 'yes am here:sent from backend')

def get_socketio():
    # global constants
    return idm_status.socketio

async def get_status():
    await read_status_file()
    return idm_status.status_track


async def start_background_tasks(app):
    """Starts process_status_updates when the app starts."""
    print("✅ Starting background tasks...")  # Debugging
    app["status_task"] = asyncio.create_task(process_status_updates())
    print(f"✅ Background task created: {app['status_task']}")


async def cleanup_background_tasks(app):
    """Cancels the background task on app shutdown."""
    app["status_task"].cancel()
    await app["status_task"]

def run_observer(app):
    idm_status.socketio = socketio.AsyncServer(cors_allowed_origins="*")
    idm_status.socketio.attach(app)
    start_observer(idm_status.socketio)

    # Start background task when the app starts
    app.on_startup.append(start_background_tasks)
    app.on_cleanup.append(cleanup_background_tasks)


    # idm_status.socketio = SocketIO(app,cors_allowed_origins="*",async_mode='threading')

    # idm_status.socketio = SocketIO(app,cors_allowed_origins="*",async_handlers=True)

    # idm_status.socketio = SocketIO(app,cors_allowed_origins="*", async_mode='eventlet')
    # idm_status.socketio = SocketIO(app,cors_allowed_origins="*",async_handlers=True,async_mode='gevent')

    # idm_status.socketio = SocketIO(app,cors_allowed_origins="*")

    # Initialize SocketIO server
    

    
    # print("inobserver",socketio)
    # socketio = SocketIO(app)
    # socketio = SocketIO(app,cors_allowed_origins="*")
    # socketio.run(app, debug=True,port=5001)
    # loop = asyncio.get_event_loop()
    # loop.run_forever()