#!/usr/bin/python3
'''Creates a new view for the link between Place objects and Amenity
    objects that handles all default RESTFul API actions
'''

from flask import abort, jsonify
from api.v1.views import app_views
from models import storage, storage_t
from models.place import Place
from models.amenity import Amenity
from os import getenv


@app_views.route('places/<place_id>/amenities',
                 methods=['GET'], strict_slashes=False)
def get_all_amenities_by_place(place_id):
    '''Retrieves the list of all Amenity instances of a Place
    '''
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    all_amenities = [amenity.to_dict() for amenity in place.amenities]
    return jsonify(all_amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def get_delete_amenity_by_id(place_id, amenity_id):
    '''Deletes an Amenity instance to a Place
    '''
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    linked_amenity = None
    for amenity in place.amenities:
        if amenity_id == amenity.id:
            linked_amenity = amenity

    if linked_amenity is None:
        abort(404)

    if storage_t == 'db':
        if amenity not in place.amenities:
            abort(404)

        place.amenities.remove(amenity)
    else:
        amenity_idx = place.amenity_ids.index(amenity_id)
        place.amenity_ids.pop(amenity_idx)

    place.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def add_amenity_to_place(place_id, amenity_id):
    '''Links an Amenity instance to a Place
    '''
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    if storage_t == 'db':
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200

        place.amenities.append(amenity)
        place.save()
        return jsonify(amenity.to_dict()), 201
    else:
        if amenity_id in place.amenity_ids:
            return jsonify(amenity.to_dict()), 200
        place.amenity_ids.push(amenity_id)
        place.save()
        return jsonify(amenity.to_dict()), 201
