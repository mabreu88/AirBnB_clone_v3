#!/usr/bin/python3
"""App module using Flask"""

from models import storage
from flask import jsonify
from models.state import State
from api.v1.views import app_views


@app_views.route('/states', methods=["GET"], strict_slashes=False)
def getStates():
    """GET route to return all States"""
    all_states = []
    for states in storage.all('State').values():
        all_states.append(states.to_dict())
    return jsonify(all_states)