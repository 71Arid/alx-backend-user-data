#!/usr/bin/env python3
"""
a class to manage the API authentication.
"""
from flask import request
from typing import List, TypeVar
from fnmatch import fnmatch


class Auth():
    """Auth class definition"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Authorization check function"""
        if path is None:
            return True
        else:
            last_index = len(path) - 1
        if excluded_paths is None or excluded_paths == []:
            return True
        if path[last_index] != "/":
            path = path + "/"
        for excluded_path in excluded_paths:
            if fnmatch(path, excluded_path):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """authorizations header function
        """
        if request is None:
            return None
        if request.headers.get("Authorization"):
            return request.headers.get("Authorization")
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """current user selector function"""
        return None
