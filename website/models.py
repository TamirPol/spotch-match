from . import db, ma
from flask_login import UserMixin

user_chat = db.Table("user_chat", 
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("chat_id", db.Integer, db.ForeignKey("chat.id"))
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    firstName = db.Column(db.String(150))
    lastName = db.Column(db.String(150))
    birthday=db.Column(db.String(150))
    age = db.Column(db.Integer)
    sport = db.Column(db.String(150))
    sex = db.Column(db.String(150))
    sameSex = db.Column(db.String(150))
    bio = db.Column(db.String(150))
    city = db.Column(db.String(150))
    chats = db.relationship("Chat", secondary=user_chat, backref='users')

class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user1 = db.Column(db.String(150))
    user2 = db.Column(db.String(150))
    room = db.Column(db.String(300), unique=True)
    messages = db.relationship("Message", backref="chat")

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(300))
    username = db.Column(db.String(150))
    chat_id = db.Column(db.Integer, db.ForeignKey("chat.id"))

class MessageSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Message
        load_instance = True