from flask import Blueprint, flash, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from .models import User, Chat, Message
from . import db
views = Blueprint("views", __name__)


@views.route("/", methods=["GET", "POST"])
@login_required
def home():
    """ chats = Chat.query.filter_by().all()
    print(chats)
    print(current_user.firstName, current_user.chats)
    print(chats[0].room)
    print(current_user.chats[0].room)

    for chat in chats:
        print("haaaaaaa",chat.room, chat.id, chat.messages, chat.users) """
    if request.method == "POST":
        newChat = Chat(room=current_user.username + "osama", user1="osama", user2="Tamirpo")
        db.session.add(newChat)
        otherUser = User.query.filter_by(username="osama").first()
        otherUser.chats.append(newChat)
        current_user.chats.append(newChat)
        db.session.commit()
    return render_template("home.html", user=current_user)

@views.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    if request.method == "POST":
        return redirect(url_for("views.editProfile"))
    print(current_user.bio)
    return render_template("profile.html", user=current_user)

@views.route("/editProfile", methods=["GET", "POST"])
@login_required
def editProfile():
    if request.method == "POST":
        username = request.form.get("username")
        firstName = request.form.get("firstName")
        lastName = request.form.get("lastName")
        birthday = request.form.get("birthday")
        sport = request.form.get("sportOption")
        sex = request.form.get("sex")
        sameSex = request.form.get("sameSex")
        bio = request.form.get("bio")
        userUsernameTaken = User.query.filter_by(username=username).first()
        if userUsernameTaken and username != current_user.username:
            flash("Username already taken!", category="dangerAlert")
        elif len(username) < 2:
            flash("Username must be greater than 1 character!", category="dangerAlert")
        elif len(firstName) < 2:
            flash("First name must be greater than 1 character!", category="dangerAlert")
        elif len(lastName) < 2:
            flash("Last name must be greater than 1 character!", category="dangerAlert")
        elif birthday == "":
            flash("Birthday is not set!", category="dangerAlert")
        elif sex is None:
            flash("Sex is not checked!", category="dangerAlert")
        elif sameSex is None:
            flash("Sex is not checked!", category="dangerAlert")
        else:
            current_user.username = username
            current_user.firstName = firstName
            current_user.lastName = lastName
            current_user.birthday = birthday
            current_user.sport = sport
            current_user.sex = sex
            current_user.sameSex = sameSex
            current_user.bio = bio
            db.session.commit()
            return redirect(url_for("views.profile"))
    return render_template("editProfile.html", user=current_user)