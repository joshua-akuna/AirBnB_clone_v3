#!/usr/bin/python3
'''Handles routes requests
'''

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    '''Returns a JSON object for status {"status": "OK"}
    '''
    return jsonify({
        'status': 'OK'
    })
