#!/usr/bin/python3
"""Flask app"""
from api.v1.views import app_views
from models import storage
from flask import jsonify, request


@app_views.route('/status', methods=['GET'])
def statusRoute():
    """Status Route"""
    if request.method == 'GET':
        return jsonify({"status": "OK"})

@app_views.route('/stats')
def count():
    """ Count objects """
    dictob = {}
    clss = {
        "Amenity": "amenities",
        "Place": "places",
        "State": "states",
        "City": "cities",
        "Review": "reviews",
        "User": "users"
    }

    for cls in clss:
        count = storage.count(cls)
        dictob[clss.get(cls)] = count
    return jsonify(dictob)
