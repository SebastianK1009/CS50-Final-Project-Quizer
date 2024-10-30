import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required, check_password, code_generator

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///quizer.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    foo = []
    codes = db.execute("SELECT DiSTINCT code FROM questions WHERE creator=?",session["user_id"])
    for code in codes:
        tmp = {}
        attempts = db.execute("SELECT COUNT(*) as attempts FROM answers WHERE code=?", code["code"])[0]["attempts"]
        x = []
        for i in range(1,4):
            n = db.execute("SELECT correct FROM questions WHERE code=? AND number=?",code["code"],i)[0]["correct"]
            if n != 0:
                n = str(round(n/attempts*100)) + "%"
                x.append(n)
            else:
                x.append("0%")
        tmp["code"] = code["code"]
        tmp["score"] = x
        tmp["attempts"] = attempts
        foo.append(tmp)

    recents = db.execute("SELECT code,mark FROM answers WHERE taker=?",session["user_id"])
    return render_template("index.html", library=foo, recents=recents)


@app.route("/create", methods=["POST","GET"])
@login_required
def create():
    if request.method == "POST":
        code = code_generator()
        q1 = request.form.get("q1")
        a1 = request.form.get("a1").lower()
        q2 = request.form.get("q2")
        a2 = request.form.get("a2").lower()
        q3 = request.form.get("q3")
        a3 = request.form.get("a3").lower()
        if not q1 or not a1 or not q2 or not a2 or not q3 or not a3:
            return apology("Please fill in all question and answers")
        db.execute("INSERT INTO questions (code,number,question,answer,creator) VALUES (?,?,?,?,?)",code,1,q1,a1,session["user_id"])
        db.execute("INSERT INTO questions (code,number,question,answer,creator) VALUES (?,?,?,?,?)",code,2,q2,a2,session["user_id"])
        db.execute("INSERT INTO questions (code,number,question,answer,creator) VALUES (?,?,?,?,?)",code,3,q3,a3,session["user_id"])
        return redirect("/")
    else:
        return render_template("create.html")


@app.route("/join", methods=["POST","GET"])
@login_required
def join():
    if request.method == "POST":
        code = request.form.get("code").upper()
        if not code:
            apology("Please Enter Code To Join!")
        questions = db.execute("SELECT code FROM questions WHERE code=?",code)
        if questions == []:
            return apology("Quiz Not Found!")
        session['code'] = code
        return redirect("/joined")
    else:
        return render_template("join.html")

@app.route("/joined", methods=["POST","GET"])
@login_required
def joined():
    questions = db.execute("SELECT * FROM questions WHERE code=?",session['code'])
    if request.method == "POST":
        if questions == []:
            return apology("Quiz Not Found!")

        mark = 0
        a1 = request.form.get("a1").lower()
        a2 = request.form.get("a2").lower()
        a3 = request.form.get("a3").lower()

        if a1 == questions[0]['answer']:
            db.execute("UPDATE questions SET correct=correct+1 WHERE code=? AND number=?", session['code'], 1)
            mark += 1
        if a2 == questions[1]['answer']:
            db.execute("UPDATE questions SET correct=correct+1 WHERE code=? AND number=?", session['code'], 2)
            mark += 1
        if a3 == questions[2]['answer']:
            db.execute("UPDATE questions SET correct=correct+1 WHERE code=? AND number=?", session['code'], 3)
            mark += 1

        db.execute("INSERT INTO answers VALUES (?,?,?)", session['code'],session['user_id'], mark)

        return redirect("/")
    else:
        return render_template("joined.html", questions=questions)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    session.clear()
    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 403)
        elif not request.form.get("password"):
            return apology("must provide password", 403)
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)
        session["user_id"] = rows[0]["id"]
        return redirect("/")
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""
    session.clear()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # check for valid entries
        if not username:
            return apology("Please Enter Username")
        elif not password:
            return apology("Please Enter Password")
        elif not confirmation:
            return apology("Please Enter Password Confirmation")
        elif password != confirmation:
            return apology("Password is different with password confirmation")
        elif db.execute("SELECT * FROM users WHERE username=?", username) != []:
            return apology("Username is taken")
        elif check_password(password) == False:
            return apology("Password Is Not Strong!")
        else:
            hpass = generate_password_hash(password)
            db.execute("INSERT INTO users (username, hash) VALUES (?,?)", username, hpass)
            return redirect("/")
    else:
        return render_template("register.html")