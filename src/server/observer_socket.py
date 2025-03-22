
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
# from watchdog.observers import Observer
# from watchdog.events import FileSystemEventHandler
from tool import read_status_file ,process_status_updates,session_manager, update_bandwidth_speed
from constants import STATUS_DOWNLOAD_FILE ,SAVE_DIR ,idm_status,SAVE_STATE_FILE
import asyncio
import socketio

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
        pass
        # observer.stop()
        # observer.join()

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
    app["session_task"] = asyncio.create_task(session_manager())
    app["speed_task"] = asyncio.create_task(update_bandwidth_speed())
    print(f"✅ Background tasks created: status_task,session_task,speed_task")


async def cleanup_background_tasks(app):
    """Cancels the background task on app shutdown."""
    app["status_task"].cancel()
    app["session_task"].cancel()
    app["speed_task"].cancel()
    await app["status_task"]
    await app["session_task"]
    await app["speed_task"]
    print(f"✅ Background tasks finished: status_task,session_task,speed_task")

def run_observer(app):
    idm_status.socketio = socketio.AsyncServer(cors_allowed_origins="*")
    idm_status.socketio.attach(app)
    # Start background task when the app starts
    app.on_startup.append(start_background_tasks)
    app.on_cleanup.append(cleanup_background_tasks)
    start_observer(idm_status.socketio)