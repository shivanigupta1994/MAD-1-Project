from flask import Flask, render_template, session
from flask_sqlalchemy import SQLAlchemy
import os


current_dir = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = 'static/'


app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(current_dir, "database.sqlite3")
#used for file upload
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 
#limit max_size of uploaded files to 16 MB   
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024     
db = SQLAlchemy()
#from model import *
db.init_app(app)
#ensures that application context sets correctly for the database
app.app_context().push() 
#secret key generated & then assigned  to app.secret_key  
app.secret_key=os.urandom(24)   


# contain route handlers & views for different parts of application i.e., HTTP requests
from controller import *
from admin import *
from API import *


#script run as main module
if __name__== "__main__":
    #host & port no. on which flask application started in debug mode    
    #app.run(host='0.0.0.0', port=8080, debug=True)   
    app.run(host='0.0.0.0', port=8080)    
 


