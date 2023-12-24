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


@app_views.get('/states/<state_id>')
def stateId(state_id):
    """GET route to return one specific State"""

    state = storage.get(State, state_id)
    if state is None:
        from flask import abort
        return abort(404)

    return state.to_dict()


@app_views.delete('/states/<state_id>')
def deleteStateId(state_id):
    """DELETE route to delete a State"""
    try:
        obj = storage.get(State, state_id)
        if obj is None:
            from flask import abort
            return abort(404)
        storage.delete(obj)
        storage.save()
        return {}, 200
    except Exception:
        from flask import abort
        return abort(404)


@app_views.post('/states/')
def postState():
    """Posts a new State"""
    from flask import request
    if request.is_json:
        data = request.get_json()
        if data.get("name") is None:
            return "Missing name", 400
        new_obj = State(**data)
        storage.new(new_obj)
        storage.save()
        return new_obj.to_dict(), 201

    return "Not a JSON", 400


@app_views.put('/states/<state_id>')
def putState(state_id):
    obj = storage.get(State, state_id)

    if obj is None:
        from flask import abort
        return abort(404)

    from flask import request
    if request.is_json:
        data = request.get_json()
        ignore_keys = ['id', 'created_at', 'updated_at']
        for key, prop in data.items():
            if key not in ignore_keys:
                setattr(obj, key, prop)
        storage.save()
        return obj.to_dict()

    return "Not a JSON", 400
