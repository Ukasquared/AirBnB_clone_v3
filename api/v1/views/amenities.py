#!/usr/bin/python3
""" handles all default
RESTFUL API actions """
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/amenities', strict_slashes=False, methods=['GET'])
def list_amenities():
    """ lists all the amenities
    in the database """
    # create a list to append states
    all_amenities = []
    # return all states from storage
    for amenities in storage.all(Amenity).values():
        all_amenities.append(amenities.to_dict())
    return jsonify(all_amenities)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['GET'])
def list_amenity_id(amenity_id):
    """list amenities associated
    with a particular id """
    amenity_w_id = storage.get(Amenity, amenity_id)
    if amenity_w_id is None:
        abort(404, description='handle_error')
    return jsonify(amenity_w_id.to_dict())


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_amenity(amenity_id):
    """ delete amenity id """
    amenity_w_id = storage.get(Amenity, amenity_id)
    if amenity_w_id is None:
        abort(404)
    amenity_w_id.delete()
    storage.save()
    return jsonify('{}'), 200


@app_views.route('/amenities', strict_slashes=False, methods=['POST'])
def post_amenity():
    """create new amenity
    object """
    amenity = request.get_json()
    if amenity is None:
        abort("Not a JSON", 400)
    if 'name' not in amenity:
        abort("Missing name", 400)
    new_amenity = Amenity(**amenity)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['PUT'])
def update_amenity(amenity_id):
    """update amenity object """
    upd_amenty = request.get_json()
    if upd_amenty is None:
        abort("Not a JSON", 400)
    amenity_w_id = storage.get(Amenity, amenity_id)
    if amenity_w_id is None:
        abort(404)
    for key, value in upd_amenty.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity_w_id, key, value)
    amenity_w_id.save()
    return jsonify(amenity_w_id.to_dict()), 200
