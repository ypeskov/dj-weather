from django.urls import path

from .views import SubscriptionView, unsubscribe, send_notification

urlpatterns = [
    path('new/', SubscriptionView.as_view(), name='subscription_new'),
    path('unsubscribe/', unsubscribe, name='subscription_delete'),
    path('notify/', send_notification, name='subscription_notify'),
]
