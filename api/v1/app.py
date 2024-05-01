#!/usr/bin/python3
""" build an api """
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv

host = getenv('HBNB_API_HOST')
port = getenv('HBNB_API_PORT')

app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')

@app.errorhandler(404)
def handle_error(e):
    """ handles app error"""
    return jsonify({"error": "Not found"}), 404

@app.teardown_appcontext
def close_session(exception):
    """ closes a sesion """
    storage.close()


if __name__ == '__main__':
    if host:
        valid_host = host
    else:
        valid_host = '0.0.0.0'
    if port:
        valid_port = int(port)
    else:
        valid_port = 5000
    app.run(host=valid_host, port=valid_port, threaded=True)
