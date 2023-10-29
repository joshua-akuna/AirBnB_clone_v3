#!/usr/bin/python3
'''Handles all RESTFul actions for City objects
'''

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State
from models.place import Place
from models.user import User
from models.amenity import Amenity


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_all_places_by_city(city_id):
    '''Retrieves the list of all Place objects associated
        with the city with city_id
    '''
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    all_places = [place.to_dict() for place in storage.all(Place).values()
                  if place.city_id == city_id]
    return jsonify(all_places)


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    '''The endpoint retrieves all Place instances depending on the
        content of the JSON in the request body
    '''
    if not request.is_json:
        abort(400, 'Not a JSON')

    payload = request.get_json()

    payload_values = []
    for key in payload:
       payload_values.extend(payload.get(key))

    all_places = []
    if len(payload) == 0 or len(payload_values) == 0:
        all_places = [place for place in storage.all(Place).values()]
    else:
        all_cities_ids = []

        # get all city ids for all specifies states
        if 'states' in payload and len(payload.get('states')) > 0:
            for state_id in payload.get('states'):
                state = storage.get(State, state_id)
                if not state:
                    continue
                all_cities_ids.extend([city.id for city in state.cities])

        # add all city ids not already in the list of city ids
        # for all specified cities
        if 'cities' in payload and len(payload.get('cities')) > 0:
            for city_id in payload.get('cities'):
                city = storage.get(City, city_id)
                if city == None:
                    continue;
                if city_id not in all_cities_ids:
                    all_cities_ids.append(city_id)

        # get all places for all city ids
        for city_id in all_cities_ids:
            city = storage.get(City, city_id)
            if not city:
                continue
            places_by_city = [place for place in city.places]
            all_places.extend(places_by_city)

    if 'amenities' in payload and len(payload.get('amenities')) > 0:
        amenity_ids = payload.get('amenities', None)
        amenities = []

        for amenity_id in amenity_ids:
            amenity = storage.get(Amenity, amenity_id)
            if not amenity:
                continue
            amenities.append(amenity)
        filtered_places = [place for place in all_places
                           if all([am in place.amenities for am in amenities])]

        place_list = []
        for place in filtered_places:
            dic = place.to_dict()
            dic.pop('amenities', None)
            place_list.append(dic)
        return jsonify(place_list)
    else:
        filtered_places = [place.to_dict() for place in all_places]
        return jsonify(filtered_places)


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
