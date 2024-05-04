#!/usr/bin/env python3
"""
new authentication system, based on
Session ID stored in database 
"""
from models.base import Base


class UserSession(Base):
    """new model for session authntication"""
    def __init__(self, *args: list, **kwargs: dict):
        """Initialiaze UserSession class"""
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')