#!/usr/bin/env python3
"""
class BasicAuth that inherits from Auth
"""
from .auth import Auth
import base64 as base
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """class BasicAuth inherits from Auth"""
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """returns the Base64 part of the
        Authorization header for a Basic
        Authentication"""
        if authorization_header is None or not type(
                authorization_header) == str:
            return None
        start_str = "Basic "
        if authorization_header[:6] == start_str:
            return authorization_header[6:]
        else:
            return None

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """returns the decoded value of a
        Base64 string base64_authorization_header"""
        if base64_authorization_header is None or not type(
                base64_authorization_header) == str:
            return None
        try:
            text = base.b64decode(base64_authorization_header)
            return text.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """returns the user email and password
        from the Base64 decoded value."""
        if decoded_base64_authorization_header is None or not type(
                decoded_base64_authorization_header) == str:
            return (None, None)
        if ":" in decoded_base64_authorization_header:
            email, password = decoded_base64_authorization_header.split(":", 1)
            return (email, password)
        else:
            return (None, None)

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """returns the User instance
        based on his email and password."""
        if user_email is None or not type(
                user_email) == str or user_pwd is None or not type(
                user_pwd) == str:
            return None
        try:
            users = User.search({'email': user_email})
        except Exception:
            return None
        if len(users) <= 0:
            return None
        if users[0].is_valid_password(user_pwd):
            return users[0]

    def current_user(self, request=None) -> TypeVar('User'):
        """retrieves the User instance for a request"""
        auth_header = self.authorization_header(request)
        b64_auth_header = self.extract_base64_authorization_header(auth_header)
        decoded_header = self.decode_base64_authorization_header(
            b64_auth_header)
        email, password = self.extract_user_credentials(decoded_header)
        return self.user_object_from_credentials(email, password)
