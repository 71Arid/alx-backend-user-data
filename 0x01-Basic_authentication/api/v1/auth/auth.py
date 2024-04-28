#!/usr/bin/env pyhthon3
""".gitignore"""
from flask import request
from typing import List, TypeVar


class Auth():
    """Auth class definition"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Authorization check function"""
        return False

    def authorization_header(self, request=None) -> str:
        """authorizations header function
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """current user selector function"""
        return None
