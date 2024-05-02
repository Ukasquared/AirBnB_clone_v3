#!/usr/bin/python3
""" handles all default
RESTFUL API actions """
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views
from flask import jsonify

@app_views.route('/amenities', strict_slashes=False, methods=['GET'] )
def list_amenities():
    """ lists all the amenities
    in the database """
    # create a list to append states
    all_amenities = []
    # return all states from storage
    for amenities in storage.all(Amenity).values():
        all_amenities.append(amenities.to_dict())
    return jsonify(all_amenities)


@app_views.route('amenities/<amenity_id>', strict_slashes=False, methods=['GET'])
def list_amenity_id(amenity_id):
    """list amenities associated
    with a particular id """
    amenity_w_id = storage.get(Amenity, amenity_id)
    if amenity_w_id == None:
        abort(404, description='handle_error')
    return jsonify(amenity_w_id.to_dict())

# @app_views.route('states/<state_id>', strict_slashes=False, method=['DELETE'])
#def delete_state(state_id):
#   """ delete state id """

