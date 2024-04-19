#!/usr/bin/python3
"""This module generates views for State objects."""

from models.city import City
from models.state import State
from models import storage
from api.v1.views import app_views
from flask import jsonify, request, abort


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def get_cities(state_id):
    """Retrieves the list of all City objects of a State"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """Returns a City object"""
    city = storage.get(City, city_id)
    if city is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """Delete a City object."""
    city = storage.get(City, city_id)
    if city is None:
        return jsonify({"error": "Not found"}), 404
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """Create a new City object."""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    if 'name' not in data:
        abort(400, description="Missing name")
    data['state_id'] = state_id
    city = City(**data)
    city.save()
    return jsonify(city.to_dict()), 201


    
@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Update a State object."""
    state = storage.get(State, state_id)
    if state is None:
        return jsonify({"error": "Not found"}), 404
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in request.json.items():
        if key not in ignore_keys:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Update a City object."""
    city = storage.get(State, state_id)
    if city is None:
        return jsonify({"error": "Not found"}), 404
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in request.json.items():
        if key not in ignore_keys:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200
