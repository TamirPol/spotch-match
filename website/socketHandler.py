from .models import Chat, Message, MessageSchema
from . import db
from flask import jsonify
#from .views import printRoom
def handleSockets(socketio, join_room, leave_room):
    @socketio.on("join-room")
    def on_join(room):
        join_room(room)
        messages = Chat.query.filter_by(room=room).first().messages
        messagesSchema = MessageSchema(many=True)
        output = messagesSchema.dump(messages)
        print(output)
        print(jsonify(output))
        socketio.emit("room-joined", data=(room))
        @socketio.on("messageSent")
        def handleMessage(msg, username):
            print(msg, room, username)
            currentChat = Chat.query.filter_by(room=room).first()
            newMessage = Message(text=msg, username=username, chat=currentChat)
            db.session.add(newMessage)
            db.session.commit()
            socketio.emit("recieve-message", msg)
        #socketio.emit("recieve-message", "haaa", to=room)