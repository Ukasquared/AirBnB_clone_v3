#!/usr/bin/python3
""" handles all default
RESTFUL API actions """
from models import storage
from models.state import State
from api.v1.views import app_views
from flask import jsonify, request, abort

@app_views.route('/states', strict_slashes=False, methods=['GET'] )
def list_states():
    """ lists all the states
    in the database """
    # create a list to append states
    all_states = []
    # return all states from storage
    for states in storage.all(State).values():
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


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['DELETE'])
def delete_state(state_id):
    """ delete state id """
    for states_key, state in storage.all(State).items():
        id_state = states_key.split('.')[1]
        if id_state == state_id:
            state.delete()
            storage.save()
            return (jsonify("{}"), 200)
    abort(404, description='handle_error')


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def post_state():
    """ add a state to database """
    state = request.get_json()
    if state == None:
        abort("Not a JSON", 400)
    if not 'name' in state:
        abort('Missing name', 404)
    # create new state
    new_state = State(**state)
    new_state.save()
    return (jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def put_state(state_id):
    """ updates the state object
    in the database """
    upd_state = request.get_json()
    if upd_state is None:
        abort("Not a JSON", 400)
    for statet_id, state in storage.all(State).items():
        id_state = statet_id.split('.')[1]
        if id_state == state_id:
            for key, val in upd_state.items():
                if key not in ['id', 'created_at', 'updated_at']:
                    setattr(state, key, val)
            state.save()
            return (jsonify(state.to_dict()), 200)
    return abort(404)
