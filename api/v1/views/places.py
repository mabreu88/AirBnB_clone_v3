#!/usr/bin/python3
"""App module using Flask"""

from models import storage
from flask import jsonify
from models.place import Place
from models.city import City
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places/',
                 methods=["GET"], strict_slashes=False)
def getPlacesOfCity(city_id):
    """GET route to return all Places of a City"""
    city = storage.get(City, city_id)
    if city is None:
        from flask import abort
        return abort(404)

    places = city.places
    dict_places = [x.to_dict() for x in places]
    return jsonify(dict_places)


@app_views.get('/places/<place_id>')
def getPlace(place_id):
    """GET route to return one specific Place"""
    place = storage.get(City, place_id)
    if place is None:
        from flask import abort
        return abort(404)

    return place.to_dict()


@app_views.delete('/places/<place_id>')
def deletePlaceId(place_id):
    """DELETE route to delete a Place"""
    try:
        obj = storage.get(Place, place_id)
        if obj is None:
            from flask import abort
            return abort(404)
        storage.delete(obj)
        storage.save()
        return {}, 200
    except Exception:
        from flask import abort
        return abort(404)


@app_views.post('/cities/<city_id>/places/')
def postPlaces(city_id):
    """Posts a new State"""
    from flask import request
    obj = storage.get(City, city_id)
    if obj is None:
        from flask import abort
        return abort(404)

    if request.is_json:
        data = request.get_json()
        if data.get("user_id") is None:
            return "Missing user_id", 400

        from models.user import User
        if storage.get(User, data.get('user_id')) is None:
            return abort(404)

        if data.get("name") is None:
            return "Missing name", 400

        new_obj = Place(**data)
        setattr(new_obj, 'city_id', city_id)
        storage.new(new_obj)
        storage.save()
        return new_obj.to_dict(), 201

    return "Not a JSON", 400


@app_views.put('/places/<place_id>')
def putPlaces(place_id):
    obj = storage.get(Place, place_id)

    if obj is None:
        from flask import abort
        return abort(404)

    from flask import request
    if request.is_json:
        data = request.get_json()
        ignore_keys = ['id', 'user_id', 'city_id',
                       'created_at', 'updated_at']
        for key, prop in data.items():
            if key not in ignore_keys:
                setattr(obj, key, prop)
        storage.save()
        return obj.to_dict()

    return "Not a JSON", 400
