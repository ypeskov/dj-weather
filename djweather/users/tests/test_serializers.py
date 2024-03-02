import pytest
from django.contrib.auth.models import User

from icecream import ic

from users.serializers import UserRegistrationSerializer, UserInfoSerializer
from core.responses.exceptions.exceptions import ApiException


def test_user_registration_serializer_success():
    valid_data = {
        'email': 'test@example.com',
        'password': 'validpassword123',
        'password2': 'validpassword123'
    }
    serializer = UserRegistrationSerializer(data=valid_data)
    assert serializer.is_valid()
    user = serializer.save()
    assert User.objects.filter(email='test@example.com').exists()
    assert user.email == 'test@example.com'


def test_user_registration_serializer_password_mismatch():
    invalid_data = {
        'email': 'testmismatch@example.com',
        'password': 'password123',
        'password2': 'password456'
    }
    serializer = UserRegistrationSerializer(data=invalid_data)
    with pytest.raises(ApiException) as e:
        serializer.is_valid(raise_exception=True)
    assert e.value.error_code == 'PASSWORD_MISMATCH'


def test_user_registration_serializer_duplicate_email(create_user):
    create_user(email='existing@example.com', username='existing@example.com', password='password123')
    invalid_data = {
        'email': 'existing@example.com',
        'password': 'newpassword123',
        'password2': 'newpassword123'
    }
    serializer = UserRegistrationSerializer(data=invalid_data)
    with pytest.raises(ApiException) as exc_info:
        serializer.is_valid(raise_exception=True)
    assert exc_info.value.error_code == 'USER_ALREADY_EXISTS'


def test_user_info_serializer(create_user):
    user = create_user(email='userinfo@example.com', first_name='Test', last_name='User',
                       username='userinfo@example.com', password='password123')
    serializer = UserInfoSerializer(instance=user)
    expected_data = {
        'id': user.id,
        'username': 'userinfo@example.com',
        'email': 'userinfo@example.com',
        'first_name': 'Test',
        'last_name': 'User'
    }
    assert serializer.data == expected_data
