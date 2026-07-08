import pytest
from tests.fixtures import auth_headers, assert_response_success, assert_response_error


def test_get_current_user(client, normal_user, user_token):
    """Test getting current user profile"""
    response = client.get(
        "/api/v1/users/me",
        headers=auth_headers(user_token)
    )
    assert_response_success(response, 200)
    data = response.json()
    assert data["email"] == "user@test.com"
    assert data["username"] == "testuser"


def test_update_current_user(client, normal_user, user_token):
    """Test updating current user profile"""
    response = client.put(
        "/api/v1/users/me",
        json={"full_name": "Updated Name"},
        headers=auth_headers(user_token)
    )
    assert_response_success(response, 200)
    data = response.json()
    assert data["full_name"] == "Updated Name"


def test_update_current_user_unauthorized(client):
    """Test updating user without authentication"""
    response = client.put(
        "/api/v1/users/me",
        json={"full_name": "Updated Name"}
    )
    assert_response_error(response, 401)


def test_list_users_admin(client, admin_user, admin_token):
    """Test listing all users as admin"""
    response = client.get(
        "/api/v1/users/users",
        headers=auth_headers(admin_token)
    )
    assert_response_success(response, 200)
    data = response.json()
    assert isinstance(data, list)


def test_list_users_forbidden(client, normal_user, user_token):
    """Test listing users as non-admin"""
    response = client.get(
        "/api/v1/users/users",
        headers=auth_headers(user_token)
    )
    assert_response_error(response, 403)
