import datetime
import re

from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    fieldsValue = {"email": "", "password": ""}
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        fieldsValue.update(email=email, password=password)
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully!", category='successAlert')
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash("Incorrect password, try again!", category='dangerAlert')
        else:
            flash("Email does not exist!", category="dangerAlert")
    return render_template("login.html", user=current_user, fieldsValue = fieldsValue)

@auth.route("sign-up", methods=["GET", "POST"])
def sign_up():
    fieldsValue = {"email": "", "username": "", "firstName": "", "lastName": "", "password1": "", "password2": "", "birthday": "", "sport": "", "sex": "", "sameSex": ""}
    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        firstName = request.form.get("firstName")
        lastName = request.form.get("lastName")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        birthday = request.form.get("birthday")
        sport = request.form.get("sportOption")
        sex = request.form.get("sex")
        sameSex = request.form.get("sameSex")
        fieldsValue.update(email=email , username=username , firstName=firstName , lastName=lastName , password1=password1 , password2=password2 , birthday=birthday , sport=sport , sex=sex , sameSex=sameSex )
        userEmailTaken = User.query.filter_by(email=email).first()
        userUsernameTaken = User.query.filter_by(username=username).first()
        if userEmailTaken:
            flash("Email already taken!", category="dangerAlert")
        elif len(email) < 4:
            flash("Email must be greater than 4 characters!", category="dangerAlert")
        elif userUsernameTaken:
            flash("Username already taken!", category="dangerAlert")
        elif len(username) < 2:
            flash("Username must be greater than 1 character!", category="dangerAlert")
        elif len(firstName) < 2:
            flash("First name must be greater than 1 character!", category="dangerAlert")
        elif len(lastName) < 2:
            flash("Last name must be greater than 1 character!", category="dangerAlert")
        elif len(password1) < 7:
            flash("Password must be greater than 6 characters!", category="dangerAlert")
        elif password1 != password2:
            flash("Passwords do not match!", category="dangerAlert")
        elif birthday == "":
            flash("Birthday is not set!", category="dangerAlert")
        elif datetime.datetime.now().year - int(birthday[0:4]) < 16:
            flash("Must be over 16 to create an account!", category="dangerAlert")
        elif sport == "False":
            flash("Sport is not chosen!", category="dangerAlert")
        elif sex is None:
            flash("Sex is not checked!", category="dangerAlert")
        elif sameSex is None:
            flash("Sex is not checked!", category="dangerAlert")
        else:
            newUser = User(email=email, username=username, firstName=firstName, lastName=lastName, password=generate_password_hash(password1, method='sha256'), birthday=birthday, age=int(birthday[0:4]), sport=sport, sex=sex, sameSex=sameSex, bio="Hi my name is " + firstName + "!")
            db.session.add(newUser)
            db.session.commit()
            flash("You have successfully created an account!", category="successAlert")
            login_user(newUser, remember=True)
            return redirect(url_for("views.home"))
    return render_template("sign_up.html", user=current_user, fieldsValue=fieldsValue)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))