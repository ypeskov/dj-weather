from rest_framework.serializers import Serializer

from icecream import ic

from core.responses.exceptions.exceptions import ApiException
from weathermanager.services.service_factory import get_weather_service
from weathermanager.services.WeatherService import WeatherService, WeatherType
from .models import Subscription


def subscribe_user_to_weather_updates(serializer: Serializer,
                                      weather_type: str = WeatherType.CURRENT.value) -> bool:
    service: WeatherService = get_weather_service()
    try:
        response = service.get_weather(serializer.validated_data['city'], weather_type)
        serializer.save()
        return response
    except ApiException as e:
        # log e
        raise e
    except Exception as e:
        # ic(e)
        # log e
        raise ApiException(
            status_code=500,
            error_code='INTERNAL_SERVER_ERROR',
            message="Error while creating subscription. Please try again later."
        )


def unsubscribe_user_to_weather_updates(serializer: Serializer) -> bool:
    subscription_id = serializer.validated_data['id']
    user = serializer.context['request'].user
    try:
        subscription = Subscription.objects.get(user=user, id=subscription_id)
        subscription.delete()
        return True
    except ApiException as e:
        raise e
    except Exception as e:
        # log e
        ic(e)
        raise ApiException(
            status_code=500,
            error_code='INTERNAL_SERVER_ERROR',
            message="Error while deleting subscription. Please try again later."
        )


def get_user_subscriptions(user) -> list:
    try:
        subscriptions = Subscription.objects.filter(user=user)
        return subscriptions
    except ApiException as e:
        raise e
    except Exception as e:
        # log e
        ic(e)
        raise ApiException(
            status_code=500,
            error_code='INTERNAL_SERVER_ERROR',
            message="Error while fetching subscriptions. Please try again later."
        )
