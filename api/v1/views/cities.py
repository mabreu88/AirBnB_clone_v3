#!/usr/bin/python3
"""App module using Flask"""

from models import storage
from flask import jsonify
from models.state import State
from models.city import City
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities',
                 methods=["GET"], strict_slashes=False)
def getCitiesOfState(state_id):
    """GET route to return all States"""
    state = storage.get(State, state_id)
    if state is None:
        from flask import abort
        return abort(404)

    cities = state.cities
    dict_cities = [x.to_dict() for x in cities]
    return jsonify(dict_cities)


@app_views.get('/cities/<city_id>')
def getCity(city_id):
    """GET route to return one specific State"""
    city = storage.get(City, city_id)
    if city is None:
        from flask import abort
        return abort(404)

    return city.to_dict()


@app_views.delete('/cities/<city_id>')
def deleteCityId(city_id):
    """DELETE route to delete a State"""
    try:
        obj = storage.get(City, city_id)
        if obj is None:
            from flask import abort
            return abort(404)
        storage.delete(obj)
        storage.save()
        return {}, 200
    except Exception:
        from flask import abort
        return abort(404)


@app_views.post('/states/<state_id>/cities/')
def postCity(state_id):
    """Posts a new State"""
    from flask import request
    obj = storage.get(State, state_id)
    if obj is None:
        from flask import abort
        return abort(404)

    if request.is_json:
        data = request.get_json()
        if data.get("name") is None:
            return "Missing name", 400
        new_obj = City(**data)
        setattr(new_obj, 'state_id', state_id)
        storage.new(new_obj)
        storage.save()
        return new_obj.to_dict(), 201

    return "Not a JSON", 400


@app_views.put('/cities/<city_id>')
def putCities(city_id):
    obj = storage.get(City, city_id)

    if obj is None:
        from flask import abort
        return abort(404)

    from flask import request
    if request.is_json:
        data = request.get_json()
        ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']
        for key, prop in data.items():
            if key not in ignore_keys:
                setattr(obj, key, prop)
        storage.save()
        return obj.to_dict()

    return "Not a JSON", 400
