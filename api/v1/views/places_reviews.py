#!/usr/bin/python3
""" handles all default
RESTFUL API actions 
in place_amenitis module
"""

from models import storage
from models.review import Review
from models.place import Place
from models.city import City
from models.user import User
from api.v1.views import app_views
from flask import jsonify, request, abort


@app_views.route('/places/<place_id>/reviews', strict_slashes=False,
                 methods=['GET'])
def list_reviews(place_id):
    """ lists all the reviews
    connected to places
    in the database """
    all_reviews = []
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    for review in storage.all(Review).values():
        if review.place_id == place_id:
            all_reviews.append(review.to_dict())
    return jsonify(all_review)


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['GET'])
def list_review_id(review_id):
    """list review associated
    with a particular id """
    review_w_id = storage.get(Review, review_id)
    if review_w_id is None:
        abort(404, description='handle_error')
    return jsonify(review_w_id.to_dict())


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_review(review_id):
    """ delete review id 
    """
    place = storage.get(Review, review_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return (jsonify('{}'), 200)


@app_views.route('/places/<place_id>/reviews', strict_slashes=False,
                 methods=['POST'])
def post_review_in_place(place_id):
    """ link review to place using
    place id """
    review = request.get_json()
    if review is None:
        abort(400, "Not a JSON")
    Place = storage.get(Place, place_id)
    if Place is None:
        abort(404)
    if 'user_id' not in place:
        abort(400, "Missing user_id")
    user = storage.get(User, place["user_id"])
    if user is None:
        abort(404)
    if 'text' not in place:
        abort(400, "Missing text")
    review['place_id'] = place_id
    new_review = Review(**review)
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['PUT'])
def update_review(review_id):
    """ update the review object """
    upd_review = request.get_json()
    if upd_review is None:
        abort(400, "Not a JSON")
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    for key, val in upd_review.items():
        if key not in ['id', 'user_id', 'place_id'
                       'created_at', 'updated_at']:
            setattr(review, key, val)
    review.save()
    return jsonify(review.to_dict()), 200
