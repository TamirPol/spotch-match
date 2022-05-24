from website import create_app
from flask_socketio import SocketIO, join_room, leave_room
from website.socketHandler import handleSockets
app = create_app()

socketio = SocketIO(app, cors_allowed_origins="*")
# Change debug to False before production

handleSockets(socketio, join_room, leave_room)

if __name__ == "__main__":
    socketio.run(app, host="localhost", port=8000, debug=True)