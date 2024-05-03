#!/usr/bin/python3
""" handles all default
RESTFUL API actions """
from models import storage
from models.city import City
from models.state import State
from api.v1.views import app_views
from flask import jsonify, request, abort

@app_views.route('/api/v1/states/<state_id>/cities', strict_slashes=False, methods=['GET'] )
def list_cities(state_id):
    """ lists all the cities
    in the database """
    # return all states from storage
    for state_id, state in storage.all(State).items():
        id_state = state_id.split('.')[1]
        if id_state == state_id:
            for city in storage.all(City).values():
                if city.State_id == state_id:
                    return jsonify(city.to_dict())
    abort(404)


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['GET'])
def list_city_id(city_id):
    """list city associated
    with a particular id """
    city_w_id = storage.get(City, city_id)
    if city_w_id is None:
        abort(404, description='handle_error')
    return jsonify(city_w_id.to_dict())

@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['DELETE'])
def delete_state(city_id):
    """ delete city id """
    for city_id, city in storage.all(City).items():
        id_city = city_id.split('.')[1]
        if id_city == city_id:
            storage.delete(city)
            storage.save()
            return (jsonify("{}"), 200)
    abort(404)

@app_views.route('/states/<state_id>/cities', strict_slashes=False, methods=['POST'])
def post_city_in_state(state_id):
    """ link city to state using
    state id """
    city = request.get_json()
    state = storage.get(State, state_id)
    if state.id != state_id:
        abort(404)
    if city == None:
        abort("Not a JSON", 400)
    if 'name' not in city:
        abort("Missing name", 400)
    city['state_id'] = state_id
    new_city = City(**city)
    new_city.save()
    return jsonify(new_city.to_dict()), 200


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['PUT'])
def update_city(city_id):
    """ update the city object """
    upd_city = request.get_json()
    if upd_city is None:
        abort("Not a JSON", 400)
    for citie_id, city in storage.all(City).items():
        id_citie = citie_id.split('.')[1]
        if id_citie == city_id:
            for key, val in upd_city.items():
                if key not in ['id', 'created_at', 'updated_at']:
                    setattr(state, key, val)
            return jsonify(city.to_dict()), 200
    return abort(404)
