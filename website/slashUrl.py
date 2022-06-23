# Imports required modules
from flask import Blueprint, redirect, url_for
from flask_login import current_user

# Initalize Blueprint
slashUrl = Blueprint("slashUrl", __name__)


@slashUrl.route("/")
def slash():
    """Called when user goes to '/', if user is authenticated redirect to home, and if not redirect to login page
        Args:
            None
        Returns:
            html template
    """
    if current_user.is_authenticated:
        return redirect(url_for("views.home"))
    return redirect(url_for("auth.login"))