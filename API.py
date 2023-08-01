#Application Programming Interface (API)
#Object Relation Mapping (ORM)
from flask_restful import Resource
from flask import request
from app import db
from model import *


class CategoryAPI(Resource):
    def get(self, category_id = None):
        if category_id:
            category = Category.query.filter_by(id=category_id).first()
            if category:
                return {"name": category.name, "image":"127.0.0.1:8080"+category.image}, 200
            else:
                return {"Message": "Category not found"}, 404
        else:
            categories = Category.query.all()
            result = dict()
            for category in categories:
                result[category.id] : {"name": category.name, "image":"127.0.0.1:8080"+category.image}
            return result

    def post(self):
        pass

    def put(self, category_id):
        pass

    def delete(self, category_id):
        pass