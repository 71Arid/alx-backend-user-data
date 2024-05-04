#!/usr/bin/env python3
"""
new authentication class SessionDBAuth
in api/v1/auth/session_db_auth.py
that inherits from SessionExpAuth
"""
from .session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """Defines how the session info is to be stored
    in db"""
    def __init__(self):
        """Initializes the class"""
        super().__init__()

    def create_session(self, user_id=None):
        """creates and stores new instance of
        UserSession and returns the Session ID"""
        if user_id is None:
            return None
        sess_id = super().create_session(user_id)
        kwargs = {
            "user_id": user_id,
            "session_id": sess_id
        }
        session = UserSession(**kwargs)
        session.save()
        return sess_id

    def user_id_for_session_id(self, session_id=None):
        """returns the User ID by requesting
        UserSession in the database based"""
        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return None
        if len(sessions) <= 0:
            return None
        cur_time = datetime.now()
        time_span = timedelta(seconds=self.session_duration)
        exp_time = sessions[0].created_at + time_span
        if exp_time < cur_time:
            return None
        return sessions[0].user_id

    def destroy_session(self, request=None):
        """destroys the UserSession based on
        the Session ID from the request cookie"""
        sess_id = self.session_cookie(request)
        try:
            sessions = UserSession.search({'session_id': sess_id})
        except Exception:
            return False
        if len(sessions) <= 0:
            return False
        sessions[0].remove()
        return True
