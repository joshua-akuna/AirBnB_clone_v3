#!/usr/bin/python3
'''Handles all RESTFul actions for City objects
'''

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_all_cities_by_state(state_id):
    '''Retrieves the list of all City objects
    '''
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    all_cities = [city.to_dict() for city in state.cities]
    return jsonify(all_cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city_by_id(city_id):
    '''Retrieves a City object by id
    '''
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city_by_id(city_id):
    '''The endpoint deletes a City instance by its id
    '''
    city_to_delete = storage.get(City, city_id)
    if city_to_delete is None:
        abort(404)
    city_to_delete.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_new_city(state_id):
    '''Creates a new City object for the State with id state_id
    '''
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    if not request.is_json:
        abort(400, 'Not a JSON')

    city_json = request.get_json()

    if 'name' not in city_json:
        abort(400, 'Missing name')

    city_json['state_id'] = state.id
    new_city = City(**city_json)
    storage.new(new_city)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    '''Updates a City object
    '''
    city_to_update = storage.get(City, city_id)

    if city_to_update is None:
        abort(404)

    if not request.is_json:
        abort(400, "Not a JSON")

    payload = request.get_json()
    for k, v in payload.items():
        if k != 'id' and k != 'created_at' and k != 'updated_at':
            setattr(city_to_update, k, v)

    city_to_update.save()
    updated_city = storage.get(City, city_id)
    return jsonify(updated_city.to_dict()), 200
