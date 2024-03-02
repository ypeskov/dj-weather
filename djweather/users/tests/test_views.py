import pytest
from rest_framework import status

from icecream import ic


def test_user_registration_success(client):
    url = '/users/register/'
    data = {
        'email': 'test@example.com',
        'password': 'testpassword123',
        'password2': 'testpassword123'
    }
    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert 'User created successfully.' in response.data['message']


def test_user_registration_password_mismatch(client):
    url = '/users/register/'
    data = {
        'email': 'testfail@example.com',
        'password': 'password123',
        'password2': 'password'
    }
    response = client.post(url, data, format='json')
    assert response.status_code == 400


def test_user_registration_duplicate_email(client, create_user):
    create_user(email='existing@example.com', username='existing@example.com', password='password123')
    url = '/users/register/'
    data = {
        'email': 'existing@example.com',
        'password': 'newpassword123',
        'password2': 'newpassword123'
    }
    response = client.post(url, data, format='json')
    assert response.status_code == 400
    assert response.data['error_code'] == 'USER_ALREADY_EXISTS'


def test_user_info(client, create_user, get_jwt_client):
    user = create_user(email='existing@example.com', username='existing@example.com', password='password123')
    client = get_jwt_client(user)
    url = '/users/info/'
    response = client.get(url)
    assert response.status_code == 200
    assert response.data['details']['email'] == user.email
    assert response.data['details']['username'] == user.username
