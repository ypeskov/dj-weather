from django.urls import resolve, reverse
from users.views import UserRegistrationView, get_user_info


def test_register_url():
    url = reverse('register')
    resolved = resolve(url)
    assert resolved.func.view_class == UserRegistrationView


def test_user_info_url():
    url = reverse('user_info')
    assert resolve(url).func == get_user_info
