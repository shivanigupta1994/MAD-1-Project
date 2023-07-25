from flask import Flask, render_template, session
from flask_sqlalchemy import SQLAlchemy
import os

current_dir = os.path.abspath(os.path.dirname(__file__))

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(current_dir, "database.sqlite3")
db = SQLAlchemy()
db.init_app(app)
app.app_context().push()
app.secret_key=os.urandom(24)

from controller import *
from admin import *

if __name__== "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)


