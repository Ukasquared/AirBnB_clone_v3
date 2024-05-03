#!/usr/bin/python3
""" handles all default
RESTFUL API actions """
from models import storage
from models.user import User
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/users', strict_slashes=False, methods=['GET'])
def list_users():
    """ lists all the users
    in the database """
    # create a list to append users
    all_users = []
    # return all users from storage
    for users in storage.all(User).values():
        all_users.append(users.to_dict())
    return jsonify(all_users)


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['GET'])
def list_user_id(user_id):
    """list user associated
    with a particular id """
    user_w_id = storage.get(User, user_id)
    if user_w_id is None:
        abort(404, description='handle_error')
    return jsonify(user_w_id.to_dict())


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['DELETE'])
def delete_user(user_id):
    """ delete user with user_id """
    user_w_id = storage.get(User, user_id)
    if user_w_id is None:
        abort(404)
    user_w_id.delete()
    storage.save()
    return (jsonify('{}'), 200)


@app_views.route('/users', strict_slashes=False, methods=['POST'])
def post_user():
    """create new user
    object """
    user = request.get_json()
    if user is None:
        abort(400, "Not a JSON", 400)
    if 'email' not in user:
        abort(400, "Missing email")
    if 'password' not in user:
        abort("Missing password")
    new_user = User(**user)
    new_user.save()
    return (jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['PUT'])
def update_user(user_id):
    """update amenity object """
    upd_user = request.get_json()
    if upd_user is None:
        abort(400, "Not a JSON")
    user_w_id = storage.get(User, user_id)
    if user_w_id is None:
        abort(404)
    for key, value in upd_user.items():
        if key not in ['id', 'email', 'created_at',
                       'updated_at']:
            setattr(user_w_id, key, value)
    user_w_id.save()
    return (jsonify(user_w_id.to_dict()), 200)
