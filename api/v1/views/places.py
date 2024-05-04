#!/usr/bin/python3
""" place module handles all default RESTFUL API actions """

from models import storage
from models.city import City
from models.state import Place
from models.user import User
from api.v1.views import app_views
from flask import jsonify, request, abort


@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=['GET'])
def list_places(city_id):
    """ lists all the places
    connected to City
    in the database """
    all_places = []
    # return all places from storage
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    for place in storage.all(Place).values():
        if place.city_id == city_id:
            all_places.append(place.to_dict())
    return jsonify(all_place)


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['GET'])
def list_place_id(place_id):
    """list place associated
    with a particular id """
    place_w_id = storage.get(Place, place_id)
    if place_w_id is None:
        abort(404, description='handle_error')
    return jsonify(place_w_id.to_dict())


@app_views.route('places/<place_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_place(place_id):
    """ delete place id """
    for place_id, place in storage.all(Place).items():
        id_place = place_id.split('.')[1]
        if id_place == place_id:
            place.delete()
            storage.save()
            return (jsonify('{}'), 200)
    abort(404)


@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=['POST'])
def post_place_in_city(city_id):
    """ link place to state using
    city id """
    place = request.get_json()
    if place is None:
        abort(400, "Not a JSON")
    city = storage.get(City, state_id)
    if city is None:
        abort(404)
    if 'user_id' not in place:
        abort(400, "Missing user_id")
    user = storage.get(User, place["user_id"])
    if user is None:
        abort(404)
    if 'name' not in place:
        abort(400, "Missing name")
    place['city_id'] = city_id
    new_place = Place(**place)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['PUT'])
def update_place(place_id):
    """ update the place object """
    upd_place = request.get_json()
    if upd_place is None:
        abort(400, "Not a JSON")
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    for key, val in upd_place.items():
        if key not in ['id', 'user_id', 'city_id'
                       'created_at', 'updated_at']:
            setattr(place, key, val)
    place.save()
    return jsonify(place.to_dict()), 200
