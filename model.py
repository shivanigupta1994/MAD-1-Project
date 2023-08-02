from app import db
from datetime import datetime

class User(db.Model):
    __tablename__="user"

    id = db.Column('id', db.Integer, primary_key = True)
    name = db.Column(db.String(50))
    address = db.Column(db.String(250))
    contact_no = db.Column(db.Integer)
    sex = db.Column(db.String(6))
    email = db.Column(db.String(100))
    password = db.Column(db.String(50))  
    
class Admin(db.Model):
    __tablename__="admin"

    id = db.Column('id', db.Integer, primary_key = True)
    name = db.Column(db.String(50))
    contact_no = db.Column(db.Integer)
    sex = db.Column(db.String(6))
    email = db.Column(db.String(100))
    password = db.Column(db.String(50))  
    
class Category(db.Model):
    __tablename__="category"

    id = db.Column('id', db.Integer, primary_key = True)
    name = db.Column(db.String(50))
    image = db.Column(db.String(50))

class Product(db.Model):
    __tablename__="product"

    id = db.Column('id', db.Integer, primary_key = True)
    name = db.Column(db.String(50))
    category = db.Column(db.Integer)
    brand = db.Column(db.String(50))
    mfg_date = db.Column(db.String(20))
    exp_date = db.Column(db.String(20))
    unit = db.Column(db.String(15))
    qty = db.Column(db.Integer)
    price_per_unit = db.Column(db.Float(15))
    image = db.Column(db.String)

class Cart(db.Model):
    __tablename__="cart"

    cart_id = db.Column('cart_id', db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)
    product_qty = db.Column(db.Integer)

class Order(db.Model):
    __tablename__="order"

    id = db.Column('id', db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    order_total = db.Column(db.Integer)
    order_time = db.Column(db.DateTime, nullable=False, default = datetime.utcnow)

class Order_details(db.Model):
    __tablename__="order_details"

    id = db.Column('id', db.Integer, primary_key=True)
    order_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)
    product_qty = db.Column(db.Integer)
    price = db.Column(db.Integer)

