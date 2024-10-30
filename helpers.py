import os
import requests
import urllib.parse

from random import randint
from flask import redirect, render_template, request, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def check_password(password):
    have_capital = False
    have_digit = False
    if len(password) < 8:
        return False
    for c in password:
        x = ord(c)
        if (x >= 65) and (x <= 90):
            have_capital = True
        elif (x >= 48) and (x <= 57):
            have_digit = True
    if have_capital == False:
        return False
    if have_digit == False:
        return False

def code_generator():
    code = ""
    for i in range(4):
        code += chr(randint(65,90))
    return code

