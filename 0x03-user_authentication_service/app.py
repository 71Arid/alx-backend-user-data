#!/usr/bin/env python3
"""
Basic flask app implementation
"""
from flask import Flask, jsonify, request, abort
from auth import Auth


app = Flask(__name__)


AUTH = Auth()


@app.route('/')
def index():
    """returns a jsonify payload"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def register_user():
    """registers a user"""
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user = AUTH.register_user(email, password)
        msg = {"email": user.email, "message": "user created"}
        return jsonify(msg)
    except Exception:
        msg = {"message": "email already registered"}
        return jsonify(msg), 400


@app.route('/sessions', methods=['POST'])
def login():
    """logs in a user"""
    email = request.form.get('email')
    password = request.form.get('password')
    user = AUTH.valid_login(email, password)
    if user is True:
        new_sess = AUTH.create_session(email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie("session_id", new_sess)
        return response
    abort(401)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
