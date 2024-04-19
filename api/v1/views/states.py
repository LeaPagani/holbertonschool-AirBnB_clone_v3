#!/usr/bin/python3
"""This module generates views for State objects."""

from models.state import State
from models import storage
from api.v1.views import app_views
from flask import jsonify

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