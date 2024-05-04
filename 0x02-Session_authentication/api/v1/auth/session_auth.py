#!/usr/bin/env python3
"""
Create a class SessionAuth that inherits from Auth.
For the moment this class will be empty.
Its the first step for creating
a new authentication mechanism:
"""
from .auth import Auth
from uuid import uuid4
from models.user import User


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

    def current_user(self, request=None):
        """returns a User instance based on a cookie value"""
        sess_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(sess_id)
        user = User.get(user_id)
        return user

    def destroy_session(self, request=None):
        """deletes the user session / logout"""
        if request is None:
            return False
        cookie = self.session_cookie(request)
        if cookie is None:
            return False
        if self.user_id_for_session_id(cookie) is None:
            return False
        self.user_id_by_session_id.pop(cookie)
        return True
