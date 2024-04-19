#!/usr/bin/python3
"""This module generates views for State objects."""

from models.state import State
from models import storage
from api.v1.views import app_views
from flask import jsonify

@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Return a list of all State objects."""
    states = [state.to_dict() for state in storage.all(State).values()]
    return jsonify(states)