import asyncio
import os
import aiohttp
# global_vars.py

STATUS_DOWNLOAD_FILE='download_state.bson'
SAVE_DIR = "./downloads"
SAVE_STATE_FILE = os.path.join(SAVE_DIR,STATUS_DOWNLOAD_FILE)
DEFAULT_DOWNLOAD_PATH = os.path.join(SAVE_DIR,STATUS_DOWNLOAD_FILE)

class App_Tracker():
    _file_lock = None  # Class-level dictionary to store locks per file
    status_track = None
    socketio = None
    _status_file_loaded = False
    # _file_lock = None  
    _status_lock = None  
    _status_queue = None
    _bandwidth_queue = None
    _session=None
    _session_event=None
    
    def __init__(self):
        self._status_lock = None
        self.status_track = {}
        self.socketio = None
        self._status_file_loaded = False
        self._file_lock = {}  
        self.__session = None
        self._status_queue = asyncio.Queue()
        self._bandwidth_queue = asyncio.Queue()
        self._status_lock = asyncio.Lock()
        self._session_event = asyncio.Event() 

    def file_lock(self, file_name):
        """Return the same lock for a given file_name."""
        if file_name not in self._locks:
            self._locks[file_name] = asyncio.Lock()
        return self._locks[file_name]

    # this should be singleton over the same event loop
    @property
    def status_lock(self):
        # if self._status_lock is None:
        # self._status_lock = asyncio.Lock()  
        return self._status_lock

    # this should be singleton over the same event loop
    @property
    def status_queue(self):
        # if self._status_queue is None:
        # self._status_queue = asyncio.Queue()
        return self._status_queue
    
    @property
    def session_event(self):
        return self._session_event
    
    @property
    def bandwidth_queue(self):
        return self._bandwidth_queue

    @property
    async def close_session(self):
        if self.__session is not None:
            print("🛑 Closing session...")
            await self.__session.close()
            self.__session = None
    
    @property
    def open_session(self):
        if self.__session is None:
            self.__session=aiohttp.ClientSession()
        return self.__session


idm_status = App_Tracker()  # Single instance