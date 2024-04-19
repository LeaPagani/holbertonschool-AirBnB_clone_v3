#!/usr/bin/python3
"""This module generates views for User objects."""

from models.user import User
from models import storage
from api.v1.views import app_views
from flask import jsonify, request


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def get_all_users():
    """Return a list of all User objects."""
    all_users = [user.to_dict() for user in storage.all(User).values()]
    return jsonify(all_users)


@app_views.route("/users/<user_id>", methods=["GET"], strict_slashes=False)
def get_user(user_id):
    """Return a User object."""
    user = storage.get(User, user_id)
    if user is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(user.to_dict())


@app_views.route("/users/<user_id>", methods=["DELETE"], strict_slashes=False)
def delete_user(user_id):
    """Delete a User object."""
    user = storage.get(User, user_id)
    if user is None:
        return jsonify({"error": "Not found"}), 404
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def create_user():
    """Create a User object."""
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    data = request.get_json()
    if "email" not in data:
        return jsonify({"error": "Missing email"}), 400
    if "password" not in data:
        return jsonify({"error": "Missing password"}), 400
    new_user = User(**data)
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def update_user(user_id):
    """Update a User object."""
    user = storage.get(User, user_id)
    if user is None:
        return jsonify({"error": "Not found"}), 404
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    ignore_keys = ["id", "email", "created_at", "updated_at"]
    for key, value in request.json.items():
        if key not in ignore_keys:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200
