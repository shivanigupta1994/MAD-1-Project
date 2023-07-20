from app import db

class User(db.Model):
    __tablename__="user"

    id = db.Column('id', db.Integer, primary_key = True, autoincrement="True")
    name = db.Column(db.String(50))
    address = db.Column(db.String(250))
    contact_no = db.Column(db.Integer)
    sex = db.Column(db.String(6))
    email = db.Column(db.String(100))
    password = db.Column(db.String(50))  
    
    