#!/usr/bin/python3
'''Handles all RESTFul actions for Amenity objects
'''

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_all_amenities():
    '''Retrieves the list of all Amenity objects
    '''
    all_amenities = [amenity.to_dict() for amenity in storage
                     .all(Amenity).values()]
    return jsonify(all_amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity_by_id(amenity_id):
    '''Retrieves a Amenity object by id
    '''
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity_by_id(amenity_id):
    '''The endpoint deletes an Amenity instance by its id
    '''
    amenity_to_delete = storage.get(Amenity, amenity_id)
    if amenity_to_delete is None:
        abort(404)
    amenity_to_delete.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_new_amenity():
    '''Creates a new Amenity instance
    '''
    if not request.is_json:
        abort(400, 'Not a JSON')

    amenity_json = request.get_json()

    if 'name' not in amenity_json:
        abort(400, 'Missing name')

    new_amenity = Amenity(**amenity_json)
    # storage.new(new_amenity)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    '''Updates an Amenity instance
    '''
    amenity_to_update = storage.get(Amenity, amenity_id)

    if amenity_to_update is None:
        abort(404)

    if not request.is_json:
        abort(400, "Not a JSON")

    payload = request.get_json()
    for k, v in payload.items():
        if k != 'id' and k != 'created_at' and k != 'updated_at':
            setattr(amenity_to_update, k, v)

    amenity_to_update.save()
    updated_amenity = storage.get(Amenity, amenity_id)
    return jsonify(updated_amenity.to_dict()), 200
