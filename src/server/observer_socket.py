import asyncio
import os
import aiofiles
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import jsonpatch
import bson

from tool import read_status_file 

from constants import STATUS_DOWNLOAD_FILE ,SAVE_DIR ,idm_status
# import constants

# from flask_cors import CORS
# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'your-secret-key'
# CORS(app,resources={r"/*":{"origins":"*"}})

SAVE_STATE_FILE = os.path.join(SAVE_DIR, STATUS_DOWNLOAD_FILE)

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

def start_observer(socketio):
    @socketio.on('connect')
    def handle_connect():
        # start_observer(socketio)
        # idm_status.status_track=await read_status_file()
        # emit('load', idm_status.status_track)
        
        if os.path.exists(SAVE_STATE_FILE):
            with open(SAVE_STATE_FILE, 'rb') as file:
                bson_data = file.read()                
                if bson_data:
                    idm_status.status_track = bson.loads(bson_data)

                emit('load', idm_status.status_track)
                # print(f"downloads_state:{downloads_state}")
        print('socket backend : Client connected')

    @socketio.on('disconnect')
    def handle_disconnect():
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
    def handle_message(msg):
        print('socket backend : Received message ', msg)
        idm_status.socketio.emit('message', 'yes am here:sent from backend')

def get_socketio():
    # global constants
    return idm_status.socketio

async def get_status():
    idm_status.status_track=await read_status_file()
    return idm_status.status_track

def run_observer(app):
    # global constants
    idm_status.socketio = SocketIO(app,cors_allowed_origins="*",async_mode='threading')
    start_observer(idm_status.socketio)
    # print("inobserver",socketio)
    # socketio = SocketIO(app)
    # socketio = SocketIO(app,cors_allowed_origins="*")
    # socketio.run(app, debug=True,port=5001)
    # loop = asyncio.get_event_loop()
    # loop.run_forever()