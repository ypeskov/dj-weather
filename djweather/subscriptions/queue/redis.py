from django.conf import settings
from redis import Redis
from celery.utils.log import get_task_logger
from contextlib import suppress

redis_broke = settings.CELERY_BROKER_URL
redis = Redis.from_url(redis_broke)

logger = get_task_logger(__name__)


def insert_cities_to_queue(cities: list, max_attempts: int = 5) -> bool:
    for attempt in range(1, max_attempts + 1):
        with suppress(Exception):
            current_cities_count: int = redis.llen('__cities__')
            updated_cities_count: int = redis.rpush('__cities__', *cities)
            if updated_cities_count - current_cities_count == len(cities):
                return True
        logger.error(f"Error while inserting cities to queue. Attempt {attempt}/{max_attempts}", exc_info=True)
    return False


def get_city_from_queue() -> str:
    city = redis.lpop('__cities__')
    return city.decode('utf-8') if city else None


def put_city_to_queue(city: str):
    redis.rpush('__cities__', city)


def get_attempts() -> int:
    attempts = redis.get('__attempts__')
    return int(attempts) if attempts else 0


def increment_attempts():
    redis.incr('__attempts__')


def reset_attempts():
    redis.set('__attempts__', 0)


def reset_city_queue():
    redis.delete('__cities__')
