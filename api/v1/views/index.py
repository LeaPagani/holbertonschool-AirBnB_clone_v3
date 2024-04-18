#!/usr/bin/python3


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

""" Flask route decorator indicates function will handle HTTP GET requests to /stats endpoint """
@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def number_objects():
    """ Retrieves the number of each objects by type """
    classes = [Amenity, City, Place, Review, State, User]
    names = ["amenities", "cities", "places", "reviews", "states", "users"]

    """ Empty dictionary to store the counts of objects by type """
    num_objs = {}
    for i in range(len(classes)):
        num_objs[names[i]] = storage.count(classes[i])

    return jsonify(num_objs)