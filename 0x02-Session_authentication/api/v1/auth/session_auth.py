#!/usr/bin/env python3
"""
Create a class SessionAuth that inherits from Auth.
For the moment this class will be empty.
Its the first step for creating
a new authentication mechanism:
"""
from .auth import Auth
from uuid import uuid4
from os import getenv


class SessionAuth(Auth):
    """
    class to implement session auth logic
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """creates a Session ID for a user_id"""
        if user_id is None or not type(user_id) == str:
            return None
        sess_id = str(uuid4())
        self.user_id_by_session_id[sess_id] = user_id
        return sess_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """returns a User ID based on a Session ID"""
        if session_id is None or not isinstance(session_id, str):
            return None
        user_id = self.user_id_by_session_id.get(session_id)
        return user_id

    def session_cookie(self, request=None):
        """returns a cookie value from a request"""
        if request is None:
            return None
        cookie = getenv("SESSION_NAME")
        response = request.cookies.get(cookie)
        return response
