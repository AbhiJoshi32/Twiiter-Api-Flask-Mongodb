from TwittterApi.app import create_app
from TwittterApi.app import socketio

fapp = create_app(debug=True)

if __name__ == '__main__':
    socketio.run(fapp)