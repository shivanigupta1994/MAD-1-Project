from flask import render_template
from app import *

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/sign-in")
def sign():
    return render_template("sign-in.html")

@app.route("/sign-up")
def sig():
    return render_template("sign-up.html")
