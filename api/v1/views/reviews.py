#!/usr/bin/python3
'''Handles all RESTFul actions for Review instances
'''

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.user import User
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_all_reviews_by_place(place_id):
    '''Retrieves the list of all Review instances associated
        with the Place instance with place_id
    '''
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    all_reviews = [review.to_dict() for review in storage.all(Review).values()
                   if review.place_id == place_id]
    return jsonify(all_reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review_by_id(review_id):
    '''Retrieves a Review instance by id
    '''
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review_by_id(review_id):
    '''The endpoint deletes a Review instance by its id
    '''
    review_to_delete = storage.get(Review, review_id)
    if review_to_delete is None:
        abort(404)
    review_to_delete.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_new_review(place_id):
    '''Creates a new Review object for the City instance with id state_id
    '''
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if not request.is_json:
        abort(400, 'Not a JSON')

    review_json = request.get_json()
    if 'user_id' not in review_json:
        abort(400, 'Missing user_id')

    user = storage.get(User, review_json.get('user_id'))
    if user is None:
        abort(404)

    if 'text' not in review_json:
        abort(400, "Mssing text")

    review_json['place_id'] = place.id
    new_review = Review(**review_json)
    # storage.new(new_review)
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    '''Updates an existing Place instance
    '''
    review_to_update = storage.get(Review, review_id)

    if review_to_update is None:
        abort(404)

    if not request.is_json:
        abort(400, "Not a JSON")

    payload = request.get_json()
    for k, v in payload.items():
        if k == 'id' or k == 'created_at' or k == 'updated_at':
            continue
        if k == 'user_id' or k == 'place_id':
            continue
        setattr(review_to_update, k, v)

    review_to_update.save()
    updated_review = storage.get(Review, review_id)
    return jsonify(updated_review.to_dict()), 200
