import os

from collections import defaultdict
from datetime import timedelta, datetime

from celery import shared_task
from celery.utils.log import get_task_logger
from django.utils import timezone
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.db.models.query import QuerySet
from django.conf import settings

from .models import Subscription
from weathermanager.services.service_factory import get_weather_service
from weathermanager.services.WeatherService import WeatherService
from .queue.redis import insert_cities_to_queue, get_city_from_queue, put_city_to_queue, get_attempts, \
    increment_attempts, reset_attempts, reset_city_queue

logger = get_task_logger(__name__)

celery_workers_count = int(settings.CELERY_WORKER_CONCURRENCY)


@shared_task
def send_subscribed_notifications(when: datetime = None):
    # if when is None, then the task is called by the scheduler
    if when is None:
        now = timezone.now()
    else:
        now = when

    subscriptions: QuerySet = Subscription.objects.filter(next_notification_datetime__lte=now)
    cities = subscriptions.values_list('city', flat=True).distinct()

    city_weather = {}
    for city in cities:
        service: WeatherService = get_weather_service()
        weather = service.get_weather(city)
        city_weather[city] = weather

    user_weather = defaultdict(list)
    for subscription in subscriptions:
        weather = city_weather[subscription.city]
        user_weather[subscription.user.id].append({
            "city": subscription.city,
            "weather": weather
        })

        # Update the next notification time if the task is NOT called with a specific time
        if when is None:
            subscription.next_notification_datetime = now.replace(minute=0, second=0, microsecond=0) + timedelta(
                hours=subscription.period_hours)
            subscription.next_notification_datetime = subscription.next_notification_datetime.replace(minute=0,
                                                                                                      second=0,
                                                                                                      microsecond=0)
            subscription.save()

    for user_id, weather_info in user_weather.items():
        send_aggregated_email.delay(user_id, weather_info)

    logger.info(f"Notifications sent for {len(subscriptions)} subscriptions")


@shared_task
def update_cache_for_upcoming_notifications():
    logger.info(f"************************** Begin Cache Update Task **************************")
    now: datetime = timezone.now()

    upcoming_notification_time: datetime = now + timedelta(hours=1)

    subscriptions: QuerySet = Subscription.objects.filter(
        next_notification_datetime__gt=now,
        next_notification_datetime__lte=upcoming_notification_time
    ).distinct('city')

    cities: list = list(subscriptions.values_list('city', flat=True).distinct())
    reset_city_queue()
    inserted: bool = insert_cities_to_queue(cities)

    if inserted:
        reset_attempts()
        logger.info(f"Cache update task inserted {len(cities)} cities to queue")
        for _ in range(celery_workers_count):  # we can run N tasks in parallel as we have 4 workers
            update_cache_for_city.delay()

    logger.info(f"Cache update task initiated for {len(cities)} cities")
    logger.info(f"************************** End Cache Update Task **************************")


@shared_task
def update_cache_for_city():
    max_attempts: int = 10
    attempts: int = get_attempts()
    # logger.info(f"Attempt {attempts}/{max_attempts}. Updating cache for city.")
    if attempts >= max_attempts:
        logger.info(f"Max attempts reached [{attempts}]. Breaking the task of updating cache for cities.")
        return

    city: str = get_city_from_queue()
    if not city:  # No city found in queue then break the task
        logger.info("No city found in queue")
        return
    service: WeatherService = get_weather_service()
    try:
        service.get_weather(city, force_cache_update=True)
    except Exception as e:
        logger.error(f"Attempt {attempts}/{max_attempts}. Error while updating cache for city {city}",
                     exc_info=False)
        put_city_to_queue(city)
        increment_attempts()

    update_cache_for_city.delay()


@shared_task
def send_aggregated_email(user_id, weather_info):
    User = get_user_model()
    user = User.objects.get(id=user_id)

    subject = "Current Weather Update"
    context = {'weather_data': weather_info}
    html_content = render_to_string('subscriptions/aggregated_email.html', context)

    email = EmailMessage(
        subject,
        html_content,
        from_email=os.environ.get('EMAIL_FROM'),
        to=[user.email],
        reply_to=[os.environ.get('EMAIL_FROM')],
    )
    email.content_subtype = "html"
    email.send()
