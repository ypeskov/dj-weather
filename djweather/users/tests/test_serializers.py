import pytest
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError

from users.serializers import UserRegistrationSerializer, UserInfoSerializer
from core.responses.exceptions.exceptions import ApiException


@pytest.mark.django_db
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


@pytest.mark.django_db
def test_user_registration_serializer_password_mismatch():
    invalid_data = {
        'email': 'testmismatch@example.com',
        'password': 'password123',
        'password2': 'password456'
    }
    serializer = UserRegistrationSerializer(data=invalid_data)
    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)


@pytest.mark.django_db
def test_user_registration_serializer_duplicate_email():
    User.objects.create_user('existing@example.com', 'existing@example.com', 'password123')
    invalid_data = {
        'email': 'existing@example.com',
        'password': 'newpassword123',
        'password2': 'newpassword123'
    }
    serializer = UserRegistrationSerializer(data=invalid_data)
    with pytest.raises(ApiException) as exc_info:
        serializer.is_valid(raise_exception=True)
    assert exc_info.value.error_code == 'USER_ALREADY_EXISTS'


@pytest.mark.django_db
def test_user_info_serializer():
    user = User.objects.create_user(username='userinfo@example.com', email='userinfo@example.com',
                                    password='testpassword', first_name='Test', last_name='User')
    serializer = UserInfoSerializer(instance=user)
    expected_data = {
        'id': user.id,
        'username': 'userinfo@example.com',
        'email': 'userinfo@example.com',
        'first_name': 'Test',
        'last_name': 'User'
    }
    assert serializer.data == expected_data
