#!/usr/bin/python3
"""App module using Flask"""

from models import storage
from models.state import State
from flask import jsonify
from api.v1.views import app_views

all_states = storage.all(State)

@app_views.route('/states/', methods=["GET"])
def getStates():
    """GET route to return all States"""
    all_states_arr = [obj.to_dict() for obj in all_states.values()]
    return all_states_arr