from threading import Thread
from flask_socketio import SocketIO, emit
import asyncio
from flask import Flask
from flask_cors import CORS
from observer_socket import run_observer ,get_status
from api import api_blueprint  # Import the blueprint
import Constants
from tool import read_status_file
import time
app = Flask(__name__)

# socketio = SocketIO(app,cors_allowed_origins="*")

app.register_blueprint(api_blueprint)  # Register the blueprint
CORS(app,resources={r"/*":{"origins":"*"}})


async def funf():
    Constants.status_tracker=await read_status_file()


# defining the flask app
async def run_flask_app():
    # global Constants
    # Constants.status_tracker=await read_status_file()
    print("FLASK & SOCKETS RUNNING OK ----->")
    
    # print("after RUN",Constants.status_tracker)
    # socketio=get_socketio()

    run_observer(app)
    app.run(debug=True, port=5001)

    

if __name__ == '__main__':
    
    # socketio_thread = Thread(target=run_observer(app))
    # socketio_thread.start()
    # run_observer(app)
  
    asyncio.run(run_flask_app())
    # run_observer(app)
    
     
    # task = asyncio.run(run_observer(app))
        
    asyncio.run(funf())
    

    # run_flask_app()
    # loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(loop)


    # Run the event loop to keep the app running
    # loop.run_forever()