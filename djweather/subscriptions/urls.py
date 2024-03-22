from django.urls import path

from .views import SubscriptionView, unsubscribe, send_test_notification, list_subscriptions, update_cache

urlpatterns = [
    path('new/', SubscriptionView.as_view(), name='subscription_new'),
    path('unsubscribe/', unsubscribe, name='subscription_delete'),
    path('notify/', send_test_notification, name='subscription_notify'),
    path('list/', list_subscriptions, name='subscription_list'),
    path('update-cache/', update_cache, name='update_cache'),
]
