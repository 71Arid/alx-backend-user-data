#!/usr/bin/env python3
"""
module to carry out intergration tests
on our user authentication
service app
"""
import requests


BASE_URL = "http://localhost:5000"


def register_user(email: str, password: str) -> None:
    """Registers a user."""
    url = f"{BASE_URL}/register"
    payload = {"email": email, "password": password}
    response = requests.post(url, json=payload)
    assert response.status_code == 200


def log_in_wrong_password(email: str, password: str) -> None:
    """Logs in with wrong password."""
    url = f"{BASE_URL}/login"
    payload = {"email": email, "password": password}
    response = requests.post(url, json=payload)
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """Logs in and returns session ID."""
    url = f"{BASE_URL}/login"
    payload = {"email": email, "password": password}
    response = requests.post(url, json=payload)
    assert response.status_code == 200
    return response.cookies.get("session_id")


def profile_unlogged() -> None:
    """Accesses profile page while unlogged."""
    url = f"{BASE_URL}/profile"
    response = requests.get(url)
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """Accesses profile page while logged."""
    url = f"{BASE_URL}/profile"
    cookies = {"session_id": session_id}
    response = requests.get(url, cookies=cookies)
    assert response.status_code == 200


def log_out(session_id: str) -> None:
    """Logs out."""
    url = f"{BASE_URL}/sessions"
    cookies = {"session_id": session_id}
    response = requests.delete(url, cookies=cookies)
    assert response.status_code == 302


def reset_password_token(email: str) -> str:
    """Requests a reset password token."""
    url = f"{BASE_URL}/reset_password"
    payload = {"email": email}
    response = requests.post(url, json=payload)
    assert response.status_code == 200
    return response.json()["reset_token"]


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Updates password using reset token."""
    url = f"{BASE_URL}/reset_password/{reset_token}"
    payload = {"email": email, "new_password": new_password}
    response = requests.put(url, json=payload)
    assert response.status_code == 200


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"

if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
