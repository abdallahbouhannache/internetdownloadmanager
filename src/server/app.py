
# import eventlet
# eventlet.monkey_patch()

from flask_socketio import SocketIO, emit
import asyncio
from flask import Flask
from flask_cors import CORS
from observer_socket import run_observer ,get_status,get_socketio
from api import api_blueprint  # Import the blueprint
# from socketio import AsyncServer
# from gevent.pywsgi import WSGIServer

# import constants
from constants import idm_status
# import pdb  debugger
# from tool import read_status_file
import time

import aiohttp

from aiohttp import web
import aiohttp_cors

# app = Flask(__name__)

app = web.Application()

# app.register_blueprint(api_blueprint)  # Register the blueprint



# CORS(app,resources={r"/*":{"origins":"*"}})

# Setup CORS
cors = aiohttp_cors.setup(
    app,
    defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
            allow_methods=["*"]  # Allow all methods (GET, POST, etc.)

        )
    }
)

app.router.add_routes(api_blueprint)

# Apply CORS to all routes
for route in app.router.routes():
    cors.add(route)


# defining the flask app
def run_flask_app():
    print("FLASK & SOCKETS RUNNING OK ----->")
    try:
        web.run_app(app, host='0.0.0.0', port=5001)
    except KeyboardInterrupt:
        idm_status.socketio.stop()
        print("Server stopped.")

if __name__ == '__main__':
    run_observer(app)
    run_flask_app()

    # asyncio.run(test_connection())

    # asyncio.run(run_flask_app())



    # flask_thread = Thread(target=run_flask_app)
    # flask_thread.start()
    # run_flask_app()
    # get_socketio()
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