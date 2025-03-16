import asyncio
import os

# global_vars.py

STATUS_DOWNLOAD_FILE='download_state.bson'
SAVE_DIR = "./downloads"
SAVE_STATE_FILE = os.path.join(SAVE_DIR,STATUS_DOWNLOAD_FILE)
DEFAULT_DOWNLOAD_PATH = os.path.join(SAVE_DIR,STATUS_DOWNLOAD_FILE)

class App_Tracker():
    status_track = {}
    socketio = None
    _status_file_loaded = False
    _file_lock = None  
    _status_lock = None  
    _status_queue = None

    def __init__(self):
        self._status_lock = None
        self.status_track = {}
        self.socketio = None
        self._status_file_loaded = False
        self._status_queue = asyncio.Queue()
        self._file_lock = None  
        self._status_lock = asyncio.Lock()   

    # this should be new/singleton over each new event loop
    @property
    def file_lock(self):
        # if self._file_lock is None:
        self._file_lock = asyncio.Lock()  # Created in the current event loop
        return self._file_lock

    # this should be singleton over all the events loops  ,
    @property
    def status_lock(self):
        # if self._status_lock is None:
        # self._status_lock = asyncio.Lock()  # Created in the current event loop
        return self._status_lock

    # this should be singleton over all the events loops  ,
    @property
    def status_queue(self):
        # if self._status_queue is None:
        # self._status_queue = asyncio.Queue() # Created in the current event loop
        return self._status_queue


idm_status = App_Tracker()  # Single instance