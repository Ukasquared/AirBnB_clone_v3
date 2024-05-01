#!/usr/bin/python3
""" index module """
from flask import jsonify
from api.v1.views import app_views
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage

@app_views.route('/status', strict_slashes=False, methods=['GET'])
def status():
    """ returns response """
    response = {"status": "OK"}
    return jsonify(response)

@app_views.route('/stats', strict_slashes=False, methods=['GET'])
def stats():
    """ returns statistics of classes"""
    classes = {"amenities": Amenity,
               "cities": City,
               "places": Place,
               "reviews": Review,
               "states": State,
               "users": User}
    cls_count = {}
    for key, value in classes.items():
        cls_count[key] = storage.count(value)
    return (cls_count)
