#!/usr/bin/env python3
"""
Create a class SessionAuth that inherits from Auth.
For the moment this class will be empty.
Its the first step for creating
a new authentication mechanism:
"""
from .auth import Auth
from uuid import uuid4


class SessionAuth(Auth):
    """
    class to implement session auth logic
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """creates a Session ID for a user_id"""
        if user_id is None or not type(user_id) == str:
            return None
        sess_id = uuid4()
        self.user_id_by_session_id[sess_id] = user_id
        return sess_id
