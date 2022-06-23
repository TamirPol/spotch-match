# Import datetime
import datetime

# Import necessery requirements
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

# Initalize Blueprint
auth = Blueprint("auth", __name__)

# Call function when /login is accessed, and both get and post requrest are permitted
@auth.route("/login", methods=["GET", "POST"])
def login():
    """
        returns login.html and lets user sign in. Checks if user entered a correct email and password and log them in if they did. Print error message if they did not
            Args:
                None
            Returns:
                html template
    """
    # Initalize fieldsValue
    fieldsValue = {"email": "", "password": ""}
    
    # Check if form is submitted
    if request.method == "POST":
        # Get values for email and passwords
        email = request.form.get("email")
        password = request.form.get("password")
        # Change fieldsValue properties to match with what user entered
        fieldsValue.update(email=email, password=password)
        # Check if user exists by email
        user = User.query.filter_by(email=email).first()
        # If user exists
        if user:
            # Unhash password and check if user entered correct password
            if check_password_hash(user.password, password):
                # Log in user, output success flash message, and redirect to views.home if password is correct
                flash("Logged in successfully!", category='successAlert')
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            else:
                # Prints error message saying password is incorrect if password doesn't match
                flash("Incorrect password, try again!", category='dangerAlert')
        else:
            # If user does not exist, print error flash message
            flash("Email does not exist!", category="dangerAlert")
    # For get request return login.html
    # Pass current_user
    # Pass fieldsValue so if user entered incorrect values all the forms won't reset
    return render_template("login.html", user=current_user, fieldsValue = fieldsValue)

@auth.route("sign-up", methods=["GET", "POST"])
def sign_up():
    """
    Let user sign up, check for any bad inputs, and create User if no errors
        Args:
            None
        Returns:
            html template
    """
    # Initialize fieldsValue
    fieldsValue = {"email": "", "username": "", "firstName": "", "lastName": "", "password1": "", "password2": "", "birthday": "", "sport": "", "city": "","sex": "", "sameSex": ""}
    # If form is submitted
    if request.method == "POST":
        # Get all information from form
        email = request.form.get("email")
        username = request.form.get("username")
        firstName = request.form.get("firstName")
        lastName = request.form.get("lastName")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        birthday = request.form.get("birthday")
        sport = request.form.get("sportOption")
        city = request.form.get("city")
        sex = request.form.get("sex")
        sameSex = request.form.get("sameSex")
        # Update fieldsValue with the informaiton passed
        fieldsValue.update(email=email , username=username , firstName=firstName , lastName=lastName , password1=password1 , password2=password2 , birthday=birthday , sport=sport , sex=sex , sameSex=sameSex, city=city )
        
        # Check if email and username are already taken
        userEmailTaken = User.query.filter_by(email=email).first()
        userUsernameTaken = User.query.filter_by(username=username).first()
        # Have error checks to check for invalid inputs. If invalid, send error flash message
        if userEmailTaken:
            flash("Email already taken!", category="dangerAlert")
        elif len(email) < 4:
            flash("Email must be greater than 4 characters!", category="dangerAlert")
        elif userUsernameTaken or username == "Spotch Match":
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
        elif str(city).capitalize() != "Ottawa" and str(city).capitalize() != "Toronto":
            flash("Currently only Ottawa and Toronto are accepted cities!", category="dangerAlert")
        elif sex is None:
            flash("Sex is not checked!", category="dangerAlert")
        elif sameSex is None:
            flash("Sex is not checked!", category="dangerAlert")
        # If all inputs are valid create a new User with the passed information, add to database and commit.
        else:
            newUser = User(email=email, username=username, firstName=firstName, lastName=lastName, password=generate_password_hash(password1, method='sha256'), birthday=birthday, age=int(birthday[0:4]), sport=sport, city=str(city).capitalize(), sex=sex, sameSex=sameSex, bio="Hi my name is " + firstName + "!")
            db.session.add(newUser)
            db.session.commit()
            # Send success flash message
            flash("You have successfully created an account!", category="successAlert")
            # Login and remember user
            login_user(newUser, remember=True)
            # Redirect user to home page
            return redirect(url_for("views.home"))
    # If get request for sign_up, return sign_up.html and pass in user and fieldsValue
    return render_template("sign_up.html", user=current_user, fieldsValue=fieldsValue)


@auth.route("/logout")
# A logged in user has to be equal to true to call this function
@login_required
def logout():
    """
    Log out user
        Args:
            None
        Returns:
            html template
    """
    logout_user()
    return redirect(url_for("auth.login"))