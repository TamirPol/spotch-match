from .models import Chat, Message, MessageSchema
from . import db
def handleSockets(socketio, join_room, leave_room):
    @socketio.on("join-room")
    def on_join(room, socketID, username):
        join_room(room)
        messages = Chat.query.filter_by(room=room).first().messages
        messagesSchema = MessageSchema(many=True)
        output = messagesSchema.dump(messages)
        socketio.emit("room-joined", data=(room, output, username.strip()), to=socketID)
        @socketio.on("messageSent")
        def handleMessage(msg, username):
            print(msg, room, username)
            currentChat = Chat.query.filter_by(room=room).first()
            newMessage = Message(text=msg, username=username, chat=currentChat)
            db.session.add(newMessage)
            db.session.commit()
            socketio.emit("recieve-message", data=(msg, username), to=room)
        #socketio.emit("recieve-message", "haaa", to=room)