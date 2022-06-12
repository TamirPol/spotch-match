from flask import Blueprint, flash, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from .models import User, Chat, Message
from . import db
views = Blueprint("views", __name__)

@login_required
@views.route("/user/profile/<username>")
def user_profile(username):
    user = User.query.filter_by(username=username).first()
    print(user)
    if user:
        return render_template("otherUserProfile.html", user=user)
    else:
        return render_template("noUserProfile.html", user=user)


@views.route("/", methods=["GET", "POST"])
@login_required
def home():
    if request.method == "POST":
        #Check sex
        #Check if already connected
        matchingUsers= User.query.filter((User.sport == current_user.sport)).filter((User.username != current_user.username)).filter((User.age - current_user.age <= 10) & (User.age - current_user.age >= -10)).limit(5).all()#.filter()
        for i in matchingUsers:
            print(i.username, i.age)
        """ newChat = Chat(room=current_user.username + "James", user1="Tamirpo", user2="James")
        db.session.add(newChat)
        otherUser = User.query.filter_by(username="James").first()
        otherUser.chats.append(newChat)
        current_user.chats.append(newChat)
        db.session.commit() """
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
    fieldsValue = {"username": current_user.username, "firstName": current_user.firstName, "lastName": current_user.lastName, "birthday": current_user.birthday, "sportOption": current_user.sport, "sex": current_user.sex, "sameSex": current_user.sameSex, "bio": current_user.bio}
    if request.method == "POST":
        username = request.form.get("username")
        firstName = request.form.get("firstName")
        lastName = request.form.get("lastName")
        birthday = request.form.get("birthday")
        sport = request.form.get("sportOption")
        sex = request.form.get("sex")
        sameSex = request.form.get("sameSex")
        bio = request.form.get("bio")
        fieldsValue.update(username=username, firstName=firstName, lastName=lastName, birthday=birthday, sportOption=sport, sex=sex, sameSex=sameSex, bio=bio)
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
            current_user.age = int(birthday[0:4])
            current_user.sport = sport
            current_user.sex = sex
            current_user.sameSex = sameSex
            current_user.bio = bio
            db.session.commit()
            return redirect(url_for("views.profile"))
    return render_template("editProfile.html", user=current_user, fieldsValue=fieldsValue)