from flask import Flask
import eventlet

from flask_socketio import SocketIO

socketio = SocketIO()

def create_app(debug=False):
    """Create an application."""
    eventlet.monkey_patch()
    app = Flask(__name__)
    app.debug = debug
    app.config['SECRET_KEY'] = 'gjr39dkjn344_!67#'
    from TwittterApi.app.api import api
    app.register_blueprint(api)
    socketio.init_app(app, async_mode='eventlet')
    return app