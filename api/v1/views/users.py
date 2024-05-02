#!/usr/bin/python3
""" handles all default
RESTFUL API actions """
from models import storage
from models.user import User
from api.v1.views import app_views
from flask import jsonify

@app_views.route('/users', strict_slashes=False, methods=['GET'] )
def list_users():
    """ lists all the states
    in the database """
    # create a list to append states
    all_users = []
    # return all states from storage
    for users in storage.all().values():
        all_users.append(users.to_dict())
    return jsonify(all_users)


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['GET'])
def list_user_id(user_id):
    """list state associated
    with a particular id """
    user_w_id = storage.get(User, user_id)
    if user_w_id == None:
        abort(404, description='handle_error')
    return jsonify(user_w_id.to_dict())

# @app_views.route('states/<state_id>', strict_slashes=False, method=['DELETE'])
#def delete_state(state_id):
#   """ delete state id """

