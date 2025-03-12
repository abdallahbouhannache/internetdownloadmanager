import asyncio
import os

# global_vars.py

STATUS_DOWNLOAD_FILE='download_state.bson'
SAVE_DIR = "./downloads"
SAVE_STATE_FILE = os.path.join(SAVE_DIR,STATUS_DOWNLOAD_FILE)
DEFAULT_DOWNLOAD_PATH = os.path.join(SAVE_DIR,STATUS_DOWNLOAD_FILE)

# idm_status.socketio = None
# file_lock = asyncio.Lock()
# status_lock = asyncio.Lock()
# status_tracker = {}

class App_Tracker():
    status_track = {}
    socketio = None
    _file_lock = None  # Private attribute, initialized later
    _status_lock = None  # Private attribute, initialized later

    def __init__(self):
        self._status_lock = None
        self.status_track = {}
        self.socketio = None
        self._file_lock = None  # Private attribute, initialized later
        self._status_lock = None  # Private attribute, initialized later

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
        self._status_lock = asyncio.Lock()  # Created in the current event loop
        return self._status_lock

idm_status = App_Tracker()  # Single instance


