#!/usr/bin/env python3
"""
class BasicAuth that inherits from Auth
"""
from .auth import Auth
import base64 as base


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
            return None
        if ":" in decoded_base64_authorization_header:
            email, password = decoded_base64_authorization_header.split(":")
            return (email, password)
        else:
            return None
