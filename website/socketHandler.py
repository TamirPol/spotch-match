# Import models and database
from .models import User, Chat, Message, MessageSchema
from . import db
def handleSockets(socketio, join_room, leave_room):
    """
    Handles sockets on the server side which include sending and recieving messages, as well as joining rooms
        Args:
            None
        Returns:
            None
    """
    @socketio.on("join-room")
    def on_join(room, socketID, username):
        """
        Called when client emits join-room requests. Join current_user to room, get the messages from the room, serialize them, and emit them back to client
        Args:
            room: string
            socketID: string
            username: string
        Returns:
            None
        """
        # Join user to room
        join_room(room)
        # Get all messages from the room
        messages = Chat.query.filter_by(room=room).first().messages
        # Serialize them using marshmallow
        messagesSchema = MessageSchema(many=True)
        output = messagesSchema.dump(messages)
        # Emit socket function to client and return room, the messages, and their username
        socketio.emit("room-joined", data=(room, output, username.strip()), to=socketID)
        @socketio.on("messageSent")
        def handleMessage(msg, username):
            """
            Called when client emits the messageSent request. Finds the chat the user sent the message in, create a new message, and add it to the chat. Finally commit the database and emit recieve-message back to client
                Args:
                    msg: str
                    username: str
                Returns:
                    None
            """
            # Filter and find chat
            currentChat = Chat.query.filter_by(room=room).first()
            # Create a new message and add it to currentChat
            newMessage = Message(text=msg, username=username, chat=currentChat)
            db.session.add(newMessage)
            db.session.commit()
            # Emit recieve-message back to room, and return the message sent and who sent it
            socketio.emit("recieve-message", data=(msg, username), to=room)