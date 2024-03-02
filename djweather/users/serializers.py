from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.responses.exceptions.exceptions import ApiException


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'password2']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise ApiException(error_code='USER_ALREADY_EXISTS',
                               status_code=400,
                               message='User with this email already exists',
                               details={'email': value})
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs.get('password2'):
            raise ApiException(error_code='PASSWORD_MISMATCH',
                               status_code=400,
                               message='Passwords do not match',
                               details={'password': 'Passwords do not match'})
        return attrs

    def save(self, **kwargs):
        email = self.validated_data['email']
        password = self.validated_data['password']

        account = User(email=email, username=email)
        account.set_password(password)
        account.save()
        return account


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
