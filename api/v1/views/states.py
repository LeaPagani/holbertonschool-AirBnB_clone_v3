#!/usr/bin/python3
"""This module generates views for State objects."""

from models.state import State
from models import storage
from api.v1.views import app_views
from flask import jsonify, request

@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    """Return a list of all State objects."""
    all_states = [state.to_dict() for state in storage.all(State).values()]
    return jsonify(all_states)

@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Return a State object."""
    state = storage.get(State, state_id)
    if state is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(state.to_dict())

@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """Delete a State object."""
    state = storage.get(State, state_id)
    if state is None:
        return jsonify({"error": "Not found"}), 404
    storage.delete(state)
    storage.save()
    return jsonify({}), 200

@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Create a new State object."""
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in request.json:
        return jsonify({"error": "Missing name"}), 400
    nstate = State(**request.get_json())
    storage.new(nstate)
    storage.save()
    return jsonify(nstate.to_dict()), 201
    
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
