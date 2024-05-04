#!/usr/bin/env python3
"""
Flask view that handles
all routes for the Session authentication.
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """
    Route:
        - POST /api/v1/auth_session/login
    Return value:
        - user login info if exists
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if email is None or email == "":
        err_msg = {"error": "email missing"}
        return jsonify(err_msg), 400
    if password is None or password == "":
        err_msg = {"error": "password missing"}
        return jsonify(err_msg), 400
    users = User.search({'email': email})
    if len(users) <= 0:
        err_msg = {"error": "no user found for this email"}
        return jsonify(err_msg), 404
    if not users[0].is_valid_password(password):
        err_msg = {"error": "wrong password"}
        return jsonify(err_msg), 401
    from api.v1.app import auth
    sess_id = auth.create_session(users[0].id)
    response = jsonify(users[0].to_json())
    cookie_name = getenv("SESSION_NAME")
    response.set_cookie(cookie_name, sess_id)
    return response


@app_views.route(
    '/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def logout():
    """
    Route:
        - DELETE /api/v1/auth_session/logout
    Return value:
        - user login info if exists
    """
    from api.v1.app import auth
    del_status = auth.destroy_session(request)
    if del_status is False:
        abort(404)
    else:
        return jsonify({}), 200
