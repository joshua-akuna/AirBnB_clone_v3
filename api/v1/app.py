#!/usr/bin/python3
''' Creates a flask applicaton server listening on 0.0.0.0,
    port 5000
'''


from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

app.register_blueprint(app_views, url_prefix='/api/v1')


@app.errorhandler(404)
def not_found(e):
    '''The endpoint handles 404 errors by returning a JSON
        object {'error': 'Not found'}
    '''
    return jsonify({'error': 'Not found'}), 404


@app.teardown_appcontext
def teardown(self):
    '''Removes all SQLAlchemy Session after handling each request
    '''
    storage.close()


if __name__ == '__main__':
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', 5000)
    app.run(host=host, port=port, threaded=True)
