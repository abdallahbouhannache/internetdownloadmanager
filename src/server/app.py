from threading import Thread
from flask_socketio import SocketIO, emit
import asyncio
from flask import Flask
from flask_cors import CORS
from observer_socket import run_observer ,get_status
from api import api_blueprint  # Import the blueprint
# import constants
from constants import idm_status
from tool import read_status_file
import time

# import pdb  debugger

app = Flask(__name__)
# idm_status.socketio = idm_status.socketio(app,cors_allowed_origins="*")

app.register_blueprint(api_blueprint)  # Register the blueprint
CORS(app,resources={r"/*":{"origins":"*"}})

async def funf():
    idm_status.status_track=await read_status_file()

# defining the flask app
async def run_flask_app():
    print("FLASK & SOCKETS RUNNING OK ----->")
    run_observer(app)
    app.run(debug=True, port=5001)
    # global constants
    # constants.idm_status.status_track=await read_status_file()
    
    # print("after RUN",constants.idm_status.status_track)
    # idm_status.socketio=get_idm_status.socketio()
    
    

if __name__ == '__main__':
    asyncio.run(run_flask_app())

    # asyncio.run(funf())

    # idm_status.socketio_thread = Thread(target=run_observer(app))
    # idm_status.socketio_thread.start()
    # run_observer(app)
  
    # run_observer(app)
    
     
    # task = asyncio.run(run_observer(app))
        
    

    # run_flask_app()
    # loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(loop)


    # Run the event loop to keep the app running
    # loop.run_forever()