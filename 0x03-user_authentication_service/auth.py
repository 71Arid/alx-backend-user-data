#!/usr/bin/env python3
"""
Define all functions related with
authorization
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4
from typing import Union


def _hash_password(password: str) -> bytes:
    """takes in a password string
    arguments and returns bytes"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """returns a string representation
    of uuid"""
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """registers users"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(email, hashed_password)
            return new_user
        raise ValueError(f"User {user.email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """validates login of a user"""
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            return False
        hashed_password = user.hashed_password
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

    def create_session(self, email: str) -> str:
        """gets the session id of a user
        specified by email"""
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            return None
        new_uuid = _generate_uuid()
        self._db.update_user(user.id, session_id=new_uuid)
        return new_uuid

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """finds user by sessionID"""
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except Exception:
            return None
        return user
