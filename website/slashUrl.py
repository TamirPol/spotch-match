from flask import Blueprint, redirect, url_for
from flask_login import current_user

slashUrl = Blueprint("slashUrl", __name__)


@slashUrl.route("/")
def slash():
    if current_user.is_authenticated:
        return redirect(url_for("views.home"))
    return redirect(url_for("auth.login"))