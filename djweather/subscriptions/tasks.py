from datetime import timedelta

from celery import shared_task
from celery.utils.log import get_task_logger
from django.utils import timezone
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string

from .models import Subscription
from weathermanager.services.service_factory import get_weather_service
from weathermanager.services.WeatherService import WeatherService

logger = get_task_logger(__name__)


@shared_task
def send_subscribed_notifications():
    now = timezone.now()
    subscriptions = Subscription.objects.filter(next_notification_datetime__lte=now)

    logger.info(f"Found {len(subscriptions)} subscriptions to notify")

    for subscription in subscriptions:
        service: WeatherService = get_weather_service()
        weather = service.get_weather(subscription.city)

        send_email.delay(subscription.user.id, weather)

        subscription.next_notification_datetime = now.replace(minute=0, second=0, microsecond=0) + timedelta(
            hours=subscription.period_hours)

        subscription.next_notification_datetime = (
            subscription.next_notification_datetime.replace(minute=0, second=0, microsecond=0))
        subscription.save()

    logger.info(f"Notifications sent for {len(subscriptions)} subscriptions")


@shared_task
def update_cache_for_upcoming_notifications():
    now = timezone.now()

    upcoming_notification_time = now + timedelta(hours=1)

    subscriptions = Subscription.objects.filter(
        next_notification_datetime__gt=now,
        next_notification_datetime__lte=upcoming_notification_time
    ).distinct('city')

    cities = subscriptions.values_list('city', flat=True).distinct()
    for city in cities:
        service: WeatherService = get_weather_service()
        service.get_weather(city)

    logger.info(f"Cache updated for {len(cities)} cities")


@shared_task
def send_email(user_id, weather_json):
    User = get_user_model()
    user = User.objects.get(id=user_id)

    subject = f"Current Weather in {weather_json['location']['name']}"
    context = {
        'city': weather_json['location']['name'],
        'current_weather': weather_json,
    }
    html_content = render_to_string('subscriptions/email.html', context)
    email = EmailMessage(
        subject,
        html_content,
        'yuriy.peskov@gmail.com',
        [user.email],
    )
    email.content_subtype = "html"
    email.send()

    # logger.info(f"Notification sent to {user.email} for city {weather_json['city']}")

    return True
