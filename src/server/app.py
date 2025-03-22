
from flask_socketio import SocketIO, emit
from flask import Flask
from flask_cors import CORS
from observer_socket import run_observer ,get_status,get_socketio
from api import api_blueprint  # Import the blueprint
from constants import idm_status
from aiohttp import web
import aiohttp_cors

app = web.Application()

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
    try:
        web.run_app(app, host='0.0.0.0', port=5001)
    except KeyboardInterrupt:
        idm_status.socketio.stop()

if __name__ == '__main__':
    run_observer(app)
    run_flask_app()