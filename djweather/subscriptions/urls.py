from django.urls import path

from .views import SubscriptionView

urlpatterns = [
    path('new/', SubscriptionView.as_view(), name='subscription_new'),
]
