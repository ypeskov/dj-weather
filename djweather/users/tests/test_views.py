import pytest
from rest_framework.test import APIClient
from rest_framework import status

from icecream import ic


@pytest.mark.django_db
def test_user_registration_success():
    client = APIClient()
    url = '/users/register/'
    data = {
        'email': 'test@example.com',
        'password': 'testpassword123',
        'password2': 'testpassword123'
    }
    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert 'User created successfully.' in response.data['message']


@pytest.mark.django_db
def test_user_registration_password_mismatch():
    client = APIClient()
    url = '/users/register/'
    data = {
        'email': 'testfail@example.com',
        'password': 'password123',
        'password2': 'password'
    }
    response = client.post(url, data, format='json')
    assert response.status_code == 400
