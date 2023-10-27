#!/usr/bin/python3
'''Handles all RESTFul actions for State objects
'''

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    '''Retrieves the list of all State objects
    '''
    all_states = [state.to_dict() for state in storage.all(State).values()]
    return jsonify(all_states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state_by_id(state_id):
    '''Retrieves a state object by id
    '''
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state_by_id(state_id):
    '''The endpoint deletes a state instance by its id
    '''
    state_to_delete = storage.get(State, state_id)
    if state_to_delete is None:
        abort(404)
    storage.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_new_state():
    '''Creates a new State object
    '''
    if not request.is_json:
        abort(400, 'Not a JSON')
    state_json = request.get_json()

    if 'name' not in state_json:
        abort(400, 'Missing name')

    new_state = State(**state_json)
    storage.new(new_state)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    '''Updates a state object
    '''
    state_to_update = storage.get(State, state_id)

    if state_to_update is None:
        abort(404)

    if not request.is_json:
        abort(400, "Not a JSON")

    payload = request.get_json()
    for k, v in payload.items():
        if k != 'id' and k != 'created_at' and k != 'updated_at':
            setattr(state_to_update, k, v)

    state_to_update.save()
    updated_state = storage.get(State, state_id)
    return jsonify(updated_state.to_dict()), 200
