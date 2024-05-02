#!/usr/bin/python3
""" handles all default
RESTFUL API actions """
from models import storage
from models.state import State
from api.v1.views import app_views
from flask import jsonify

@app_views.route('/states', strict_slashes=False, methods=['GET'] )
def list_states():
    """ lists all the states
    in the database """
    # create a list to append states
    all_states = []
    # return all states from storage
    for states in storage.all().values():
        all_states.append(states.to_dict())
    return jsonify(all_states)


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def list_states_id(state_id):
    """list state associated
    with a particular id """
    state_w_id = storage.get(State, state_id)
    if state_w_id == None:
        abort(404, description='handle_error')
    return jsonify(state_w_id.to_dict())

# @app_views.route('states/<state_id>', strict_slashes=False, method=['DELETE'])
#def delete_state(state_id):
#   """ delete state id """

