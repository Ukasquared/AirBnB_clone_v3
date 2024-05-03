#!/usr/bin/python3
""" handles all default
RESTFUL API actions """
from models import storage
from models.city import City
from models.state import Place
from models.user import User
from api.v1.views import app_views
from flask import jsonify

@app_views.route('/cities/<city_id>/places', strict_slashes=False, methods=['GET'] )
def list_places(city_id):
    """ lists all the places
    connected to City
    in the database """
    # return all places from storage
    for city_id, city in storage.all(City).items():
        id_city = city_id.split('.')[1]
        if id_city == city_id:
            for place in storage.all(Place).values():
                if place.id == city_id:
                    return jsonify(place.to_dict())
    abort(404)


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['GET'])
def list_city_id(place_id):
    """list place associated
    with a particular id """
    place_w_id = storage.get(Place, place_id)
    if place_w_id == None:
        abort(404, description='handle_error')
    return jsonify(place_w_id.to_dict())

@app_views.route('places/<place_id>', strict_slashes=False, methods=['DELETE'])
def delete_place(place_id):
    """ delete place id """
    for place_id, place in storage.all(Place).items():
        id_place = place_id.split('.')[1]
        if id_place == place_id:
            place.delete()
            return ({}, 200)
    abort(404)

@app_views.route('/cities/<city_id>/places', strict_slashes=False, methods=['POST'])
def post_place_in_city(city_id):
    """ link place to state using
    city id """
    place = request.get_json()
    city = storage.get(City, state_id)
    if city.id != city_id:
        abort(404)
    if place is None:
        abort("Not a JSON", 400)
    if 'user_id' not in place:
        abort("Missing user_id", 400)
    user = storage.get(User, place[user_id])
    if user is None:
        abort(404)
    if 'name' not in city:
        abort("Missing name", 400)
    place['city_id'] = city_id
    new_place = Place(**place)
    new_place.save()
    return (new_place.to_dict(), 201)


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['PUT'])
def update_city(place_id):
    """ update the place object """
    upd_place = request.get_json()
    if upd_place is None:
        abort("Not a JSON", 400)
    for place_id, place in storage.all(Place).items():
        id_place = place_id.split('.')[1]
        if id_place == place_id:
        for key, val in upd_place.items():
            if key not in ['id', 'user_id', 'created_at', 'updated_at']:
                setattr(state, key, val)
            return (place.to_dict(), 200)
    return abort(404)
