from django.urls import path

from .views import SubscriptionView, unsubscribe

urlpatterns = [
    path('new/', SubscriptionView.as_view(), name='subscription_new'),
    path('unsubscribe/', unsubscribe, name='subscription_delete'),
]
