#!/usr/bin/env python3
"""
this module adds an expiry
date a Session ID.
"""
from .session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """class that describe the expiration
    logic of a Session ID"""
    def __init__(self):
        """inititalizes SessionEXAuth class"""
        try:
            self.session_duration = int(
                getenv("SESSION_DURATION"))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """overloads superclass method
        create_session"""
        sess_id = super().create_session(user_id)
        if not sess_id:
            return None
        sess_dict = {"user_id": user_id, "created_at": datetime.now()}
        self.user_id_by_session_id[sess_id] = sess_dict
        return sess_id

    def user_id_for_session_id(self, session_id=None):
        """overloads superclass method
        user_id_for_session_id"""
        if session_id is None:
            return None
        if self.user_id_by_session_id.get(
                session_id) is None:
            return None
        sess_dict = self.user_id_by_session_id[session_id]
        if self.session_duration <= 0:
            return sess_dict.get("user_id")
        if "created_at" not in sess_dict:
            return None
        current_time = datetime.now()
        session_endtime = sess_dict["created_at"] + timedelta(
            seconds=self.session_duration)
        if session_endtime < current_time:
            return None
        else:
            return sess_dict.get("user_id")
