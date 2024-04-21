#!/usr/bin/python3
"""This module generates views for Place objects."""
from flask import jsonify, request, abort
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from api.v1.views import app_views


@app_views.route("/cities/<city_id>/places",
                 methods=["GET"], strict_slashes=False)
def get_all_places(city_id):
    """Return a list of all Place objects in a City."""
    city = storage.get(City, city_id)
    if city is None:
        return jsonify({"error": "Not found"}), 404
    all_places = [place.to_dict() for place in city.places]
    return jsonify(all_places)


@app_views.route("/places/<place_id>",
                 methods=["GET"], strict_slashes=False)
def get_place(place_id):
    """Return a Place object."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/cities/<city_id>/places",
                 methods=["POST"], strict_slashes=False)
def create_place(city_id):
    """Create a Place object."""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    if not request.is_json:
        abort(400, "Not a JSON")
    data = request.get_json()

    if "user_id" not in data:
        abort(400, "Missing user_id")
    user = storage.get(User, data["user_id"])
    if user is None:
        abort(404)

    if "name" not in data:
        abort(400, "Missing name")

    data["city_id"] = city_id
    new_place = Place(**data)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route("/places/<place_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_place(place_id):
    """Delete a Place object."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>",
                 methods=["PUT"], strict_slashes=False)
def update_place(place_id):
    """Update a Place object."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if not request.is_json:
        abort(400, "Not a JSON")
    for key, value in request.get_json().items():
        if key not in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200
