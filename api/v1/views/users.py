#!/usr/bin/python3
'''Handles all RESTFul actions for User objects
'''

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_users():
    '''Retrieves the JSON list of all User instances
    '''
    all_users = [user.to_dict() for user in storage.all(User).values()]
    return jsonify(all_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user_by_id(user_id):
    '''Retrieves a User object by id
    '''
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user_by_id(user_id):
    '''The endpoint deletes a User instance by its id
    '''
    user_to_delete = storage.get(User, user_id)
    if user_to_delete is None:
        abort(404)
    user_to_delete.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_new_user():
    '''Creates a new User instance
    '''
    if not request.is_json:
        abort(400, 'Not a JSON')

    user_json = request.get_json()

    if 'email' not in user_json:
        abort(400, 'Missing email')

    if 'password' not in user_json:
        abort(400, 'Missing password')

    new_user = User(**user_json)
    # storage.new(new_state)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    '''Updates a User instance
    '''
    user_to_update = storage.get(User, user_id)

    if user_to_update is None:
        abort(404)

    if not request.is_json:
        abort(400, "Not a JSON")

    payload = request.get_json()

    for k, v in payload.items():
        if k == 'id' or k == 'email' or k == 'created_at' or k == 'updated_at':
            continue
        setattr(user_to_update, k, v)

    user_to_update.save()
    updated_user = storage.get(User, user_id)
    return jsonify(updated_user.to_dict()), 200
    # return jsonify(user_to_update.to_dict()), 200
