#!/usr/bin/env python3
"""
class BasicAuth that inherits from Auth
"""
from .auth import Auth


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
