#!/usr/bin/python3
"""Index view for API v1."""

from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage
from . import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'])
def status():
    """Return the status of the API."""
    return jsonify({"status": "OK"})


@app_views.route("/stats", methods=["GET"])
def stats():
    """Return the status of the API in this format."""
    classes = {
        "amenities": Amenity,
        "cities": City,
        "places": Place,
        "reviews": Review,
        "states": State,
        "users": User,
    }
    stats = {cls_key: storage.count(cls_val) for cls_key,
             cls_val in classes.items()}
    return jsonify(stats)
