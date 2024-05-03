#!/usr/bin/python3
""" handles all default
RESTFUL API actions """
from models import storage
from models.city import City
from models.state import State
from api.v1.views import app_views
from flask import jsonify, request, abort


@app_views.route('/states/<state_id>/cities',
                 strict_slashes=False, methods=['GET'])
def list_cities(state_id):
    """ lists all the cities
    in the database """
    all_cities = []
    found = False
    # return all states from storage
    for statet_id in storage.all(State).keys():
        id_state = statet_id.split('.')[1]
        if id_state == state_id:
            found = True
            for city in storage.all(City).values():
                if city.state_id == state_id:
                    all_cities.append(city.to_dict())
    if not found:
        abort(404)
    return jsonify(all_cities)


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['GET'])
def list_city_id(city_id):
    """list city associated
    with a particular id """
    city_w_id = storage.get(City, city_id)
    if city_w_id is None:
        abort(404, description='handle_error')
    return jsonify(city_w_id.to_dict())


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['DELETE'])
def delete_city(city_id):
    """ delete city id """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return (jsonify("{}"), 200)


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['POST'])
def post_city_in_state(state_id):
    """ link city to state using
    state id """
    city = request.get_json(silent=True)
    if city is None:
        abort(400, "Not a JSON")
    if 'name' not in city:
        abort(400, "Missing name")
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    city['state_id'] = state_id
    new_city = City(**city)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['PUT'])
def update_city(city_id):
    """ update the city object """
    upd_city = request.get_json(silent=True)
    if upd_city is None:
        abort(400, "Not a JSON")
    found = False
    for citie_id, city in storage.all(City).items():
        id_citie = citie_id.split('.')[1]
        if id_citie == city_id:
            found = True
            for key, val in upd_city.items():
                if key not in ['id', 'created_at', 'updated_at']:
                    setattr(city, key, val)
        if found:
            city.save()
            return jsonify(city.to_dict()), 200
    return abort(404)
