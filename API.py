#Application Programming Interface (API)
#API is a way for two or more computer programs to communicate with each other.
#Object Relational Mapping (ORM)
#ORM provides a bridge b/w relational database tables, relationships & fields and Python objects

from app import *
from model import *
from flask import request, jsonify
import os


@app.route("/category_api/<int:id>", methods=["GET", "PUT", "DELETE"])
def category_api(id):
    if request.method=="GET":
        category = Category.query.filter_by(id=id).first()
        result = {"name": category.name, "image": "127.0.0.1:8080"+category.image}
        return jsonify(result)
    
    elif request.method=="PUT":
        data = request.get_json()
        name = data.get("name")

        category = Category.query.filter_by(id=id).first()
        if category:
            category.name = name
            db.session.commit()
            return {"Message": "Category updated successfully!"}, 200
        else:
            return {"Message": "Category not found"}, 404
        
    elif request.method=="DELETE":
        Product.query.filter_by(category=id).delete()
        Category.query.filter_by(id=id).delete()
        db.session.commit()
        return {"Message": "Category deleted successfully..."}, 200
    
@app.route("/category_api", methods=["GET", "POST"])
def category_api_1():
    if request.method=="GET":
        categories = Category.query.all()
        result = dict()
        for category in categories:
            result[category.id] = {"name": category.name, "image": "127.0.0.1:8080"+category.image}
        return jsonify(result)
    
    elif request.method=="POST":
        data = request.get_json()
        name = data.get("name")

        update_category = Category(name=name, image="/static/temp.jpeg")
        db.session.add(update_category)
        db.session.flush()
        db.session.commit()
        return {"Message": "Category created successfully!"}, 200
    
        

@app.route("/product_api/<int:id>", methods=["GET", "PUT", "DELETE"])
def product_api(id):
    if request.method=="GET":
        product = Product.query.filter_by(id=id).first()
        result = {"name": product.name, "brand": product.brand, "category_id": product.category, "mfg_date": product.mfg_date, "exp_date": product.exp_date, "unit": product.unit, "quantity": product.qty, "price": product.price_per_unit, "image": "127.0.0.1:8080"+product.image}
        return jsonify(result)
    
    elif request.method=="PUT":
        data = request.get_json()
        name = data.get("name")
        brand = data.get("brand")
        category_id = data.get("category_id")
        mfg_date = data.get("mfg_date")
        exp_date  = data.get("exp_date")
        unit = data.get("unit")
        quantity = data.get("quantity")
        price = data.get("price")

        product = Product.query.filter_by(id=id).first()
        if product:
            product.name = name
            product.brand = brand
            product.category = category_id
            product.mfg_date = mfg_date
            product.exp_date = exp_date
            product.unit = unit
            product.qty = quantity
            product.price_per_unit = price
            db.session.commit()
            return {"Message": "Category updated successfully!"}, 200
        else:
            return {"Message": "Category not found"}, 404
        
    elif request.method=="DELETE":
        product = Product.query.filter_by(id=id).delete()
        db.session.commit()
        return {"Message": "Product deleted successfully..."}, 200
    
@app.route("/product_api", methods=["GET", "POST"])
def product_api_1():
    if request.method=="GET":
        products = Product.query.all()
        result = dict()
        for product in products:
            result[product.id] = {"name": product.name, "brand": product.brand, "category_id": product.category, "mfg_date": product.mfg_date, "exp_date": product.exp_date, "unit": product.unit, "quantity": product.qty, "price": product.price_per_unit, "image": "127.0.0.1:8080"+product.image}
        return jsonify(result)
    
    elif request.method=="POST":
        #in bracket, variable from json (postman)
        #left side, just variable
        data = request.get_json()
        name = data.get("name")
        brand = data.get("brand")
        category = data.get("category_id")
        mfg_date = data.get("mfg_date")
        exp_date = data.get("exp_date")
        unit = data.get("unit")
        qty = data.get("quantity")
        price_per_unit = data.get("price")
        #left side variables from model & right side variables from above
        update_product = Product(name= name, brand= brand, category=category, mfg_date= mfg_date, exp_date= exp_date, unit= unit, qty=qty, price_per_unit= price_per_unit, image= "/static/temp.jpeg")
        db.session.add(update_product)
        db.session.flush()
        db.session.commit()
        return {"Message": "Product created successfully!"}, 200
    