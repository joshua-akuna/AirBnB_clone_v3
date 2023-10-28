#!/usr/bin/python3
'''Handles all RESTFul actions for City objects
'''

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_all_places_by_city(city_id):
    '''Retrieves the list of all Place objects associated
        with the city with city_id
    '''
    print(city_id)
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    all_places = [place.to_dict() for place in storage.all(Place).values()
                  if place.city_id == city_id]
    return jsonify(all_places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place_by_id(place_id):
    '''Retrieves a Place object by id
    '''
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place_by_id(place_id):
    '''The endpoint deletes a Place instance by its id
    '''
    place_to_delete = storage.get(Place, place_id)
    if place_to_delete is None:
        abort(404)
    place_to_delete.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_new_place(city_id):
    '''Creates a new Place object for the City instance with id state_id
    '''
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    if not request.is_json:
        abort(400, 'Not a JSON')

    place_json = request.get_json()
    if 'user_id' not in place_json:
        abort(400, 'Missing user_id')

    user = storage.get(User, place_json.get('user_id'))
    if user is None:
        abort(404)

    if 'name' not in place_json:
        abort(400, "Mssing name")

    place_json['city_id'] = city.id
    new_place = Place(**place_json)
    storage.new(new_place)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    '''Updates an existing Place instance
    '''
    place_to_update = storage.get(Place, place_id)

    if place_to_update is None:
        abort(404)

    if not request.is_json:
        abort(400, "Not a JSON")

    payload = request.get_json()
    for k, v in payload.items():
        if k == 'id' or k == 'created_at' or k == 'updated_at':
            continue
        if k == 'user_id' or k == 'city_id':
            continue
        setattr(place_to_update, k, v)

    place_to_update.save()
    updated_place = storage.get(Place, place_id)
    return jsonify(updated_place.to_dict()), 200
