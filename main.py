# Import create_app, socketio module, and handleSockets function from socketHandler file
from website import create_app
from flask_socketio import SocketIO, join_room, leave_room
from website.socketHandler import handleSockets

# set app equal to create_app()
app = create_app()

# Create a flask socketio server
socketio = SocketIO(app, cors_allowed_origins="*")
# Call handleSockets function and pass the flask socketio server with socket functions
handleSockets(socketio, join_room, leave_room)

# Run application
if __name__ == "__main__":
    socketio.run(app, host="localhost", port=8000, debug=True)