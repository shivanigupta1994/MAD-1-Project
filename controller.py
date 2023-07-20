from flask import render_template, session
from app import *
from model import *

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/sign-in")
def sign():
    if 'user_id' in session:
        userid = session['user_id']
        return render_template("index.html")
    return render_template("sign-in.html")

@app.route("/sign-up")
def sign():
    return render_template("sign-up.html")


