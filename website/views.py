from flask import Blueprint, flash, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from .models import User, Chat, Message
from . import db
import datetime

views = Blueprint("views", __name__)
@login_required
@views.route("/user/profile/<username>")
def user_profile(username):
    user = User.query.filter_by(username=username).first()
    if user:
        return render_template("otherUserProfile.html", user=current_user, otherUser=user, currentYear=datetime.datetime.now().year)
    else:
        return render_template("noUserProfile.html", user=current_user)


@views.route("/", methods=["GET", "POST"])
@login_required
def home():
    if request.method == "POST":
        matchingUsers= User.query.filter((User.sport == current_user.sport)).filter((User.city == current_user.city)).filter((User.username != current_user.username)).filter((User.age - current_user.age <= 10) & (User.age - current_user.age >= -10)).filter((User.sex == current_user.sex) | ((User.sameSex == "no") & (current_user.sameSex == "no"))).all()
        fiveMatchingUsers = []
        for user in matchingUsers:
            if len(fiveMatchingUsers) > 5:
                break
            if len(current_user.chats) == 0:
                fiveMatchingUsers.append(user)
            chatExists = False
            for currentChat in current_user.chats:        
                if currentChat in user.chats:
                    chatExists = True
            if not chatExists:
                fiveMatchingUsers.append(user)
        if len(fiveMatchingUsers) == 0:
            flash("Sorry, there currently aren't any other users who match your preferences, try again later!", category="dangerAlert")    
        else:
            flash("New users have been connected to your account!!", category="successAlert")
        for user in fiveMatchingUsers:
            newChat = Chat(room=current_user.username + user.username, user1=current_user.username, user2=user.username)
            db.session.add(newChat)
            newMessage= Message(text="You two have matched!", username="Spotch Match", chat=newChat)
            db.session.add(newMessage)
            current_user.chats.append(newChat)
            user.chats.append(newChat)
            db.session.commit()
            
    return render_template("home.html", user=current_user)

@views.route("/searchForUser", methods=["POST"])
def searchedForUser():
    user = request.form.get("findUsername")
    searchUser = User.query.filter_by(username=user).first()
    if searchUser is None:
        flash("User does not exist!", category='dangerAlert')
    elif searchUser == current_user:
        flash("Do not enter your username!", category='dangerAlert')
    else:
        userAlreadyConnected = False
        for chat in current_user.chats:
            if chat in searchUser.chats:
                userAlreadyConnected = True
                flash("User is already connected to you!", category='dangerAlert')
        if not userAlreadyConnected:
            newChat = Chat(room=current_user.username + searchUser.username, user1=current_user.username, user2=searchUser.username)
            db.session.add(newChat)
            newMessage= Message(text=current_user.username + " wanted to chat!", username="Spotch Match", chat=newChat)
            db.session.add(newMessage)
            current_user.chats.append(newChat)
            searchUser.chats.append(newChat)
            db.session.commit()
            flash("New chat created", category='successAlert')
    return redirect(url_for("views.home"))

@views.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    print(current_user)
    if request.method == "POST":
        return redirect(url_for("views.editProfile"))
    return render_template("profile.html", user=current_user, currentYear = datetime.datetime.now().year)

@views.route("/editProfile", methods=["GET", "POST"])
@login_required
def editProfile():
    fieldsValue = {"username": current_user.username, "firstName": current_user.firstName, "lastName": current_user.lastName, "birthday": current_user.birthday, "sportOption": current_user.sport, "city": current_user.city,"sex": current_user.sex, "sameSex": current_user.sameSex, "bio": current_user.bio}
    if request.method == "POST":
        username = request.form.get("username")
        firstName = request.form.get("firstName")
        lastName = request.form.get("lastName")
        birthday = request.form.get("birthday")
        city = request.form.get("city")
        sport = request.form.get("sportOption")
        sex = request.form.get("sex")
        sameSex = request.form.get("sameSex")
        bio = request.form.get("bio")
        fieldsValue.update(username=username, firstName=firstName, lastName=lastName, birthday=birthday, sportOption=sport, sex=sex, sameSex=sameSex, bio=bio, city=city)
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
        elif str(city).capitalize() != "Ottawa" and str(city).capitalize() != "Toronto":
            flash("Currently only Ottawa and Toronto are accepted cities!", category="dangerAlert")
        elif sex is None:
            flash("Sex is not checked!", category="dangerAlert")
        elif sameSex is None:
            flash("Sex is not checked!", category="dangerAlert")
        else:
            current_user.username = username
            current_user.firstName = firstName
            current_user.lastName = lastName
            current_user.birthday = birthday
            current_user.age = int(birthday[0:4])
            current_user.sport = sport
            current_user.sex = sex
            current_user.sameSex = sameSex
            current_user.bio = bio
            current_user.city=str(city).capitalize()
            db.session.commit()
            return redirect(url_for("views.profile"))
    return render_template("editProfile.html", user=current_user, fieldsValue=fieldsValue)