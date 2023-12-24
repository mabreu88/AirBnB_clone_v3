#!/usr/bin/python3
"""App module using Flask"""

from models import storage
from flask import jsonify
from models.user import User
from api.v1.views import app_views


@app_views.get('/users/')
def getUsers():
    """GET route to return all Users"""
    users = storage.all(User)
    dict_users = [u.to_dict() for u in users.values()]
    return jsonify(dict_users)


@app_views.get('/users/<user_id>')
def getUserById(user_id):
    """GET route to return one specific User"""
    user = storage.get(User, user_id)
    if user is None:
        from flask import abort
        return abort(404)

    return user.to_dict()


@app_views.delete('/users/<user_id>')
def deleteUser(user_id):
    """DELETE route to delete a User"""
    try:
        obj = storage.get(User, user_id)
        if obj is None:
            from flask import abort
            return abort(404)
        storage.delete(obj)
        storage.save()
        return {}, 200
    except Exception:
        from flask import abort
        return abort(404)


@app_views.post('/api/v1/users')
def postUser():
    """Posts a new State"""
    from flask import request

    if request.is_json:
        data = request.get_json()

        if data.get("email") is None:
            return "Missing email", 400

        if data.get("password") is None:
            return "Missing password", 400

        new_obj = User(**data)
        storage.new(new_obj)
        storage.save()
        return new_obj.to_dict(), 201

    return "Not a JSON", 400


@app_views.put('/users/<user_id>')
def putUser(user_id):
    obj = storage.get(User, user_id)

    if obj is None:
        from flask import abort
        return abort(404)

    from flask import request
    if request.is_json:
        data = request.get_json()
        ignore_keys = ['id', 'email', 'created_at', 'updated_at']
        for key, prop in data.items():
            if key not in ignore_keys:
                setattr(obj, key, prop)
        storage.save()
        return obj.to_dict(), 200

    return "Not a JSON", 400
