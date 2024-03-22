from datetime import datetime, timedelta

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.utils import timezone

from icecream import ic

from core.responses.exceptions.exceptions import ApiException
from core.responses.successes.successes import ApiSuccessResponse
from .serializers import SubscriptionSerializer, UnsubscriptionSerializer
from .services import subscribe_user_to_weather_updates, unsubscribe_user_to_weather_updates, get_user_subscriptions
from .tasks import update_cache_for_upcoming_notifications, send_subscribed_notifications


class SubscriptionView(APIView):
    def post(self, request):
        serializer = SubscriptionSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            try:
                subscribe_user_to_weather_updates(serializer)

                data, status_code = ApiSuccessResponse(
                    message="Subscription created successfully.",
                    details=serializer.data
                ).to_response()
                return Response(data=data, status=status_code)
            except ApiException as e:
                # log e
                raise e
            except Exception as e:
                # log e
                raise ApiException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    error_code='INTERNAL_SERVER_ERROR',
                    message="Error while creating subscription. Please try again later."
                )


@api_view(['POST'])
def unsubscribe(request):
    serializer = UnsubscriptionSerializer(data=request.data, context={'request': request})
    if serializer.is_valid(raise_exception=True):
        try:
            unsubscribe_user_to_weather_updates(serializer)
            data, status_code = ApiSuccessResponse(
                message="Subscription deleted successfully.",
                details=serializer.data
            ).to_response()
            return Response(data=data, status=status_code)
        except ApiException as e:
            # log e
            raise e
        except Exception as e:
            # log e
            ic(e)
            raise ApiException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                error_code='INTERNAL_SERVER_ERROR',
                message="Error while deleting subscription. Please try again later."
            )


@api_view(['GET'])
def list_subscriptions(request):
    """
    List all subscriptions of the user.
    """
    subscriptions = get_user_subscriptions(request.user)
    serializer = SubscriptionSerializer(subscriptions, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def send_test_notification(request):
    now: datetime = timezone.now()
    upcoming_notification_time: datetime = now + timedelta(hours=1)
    send_subscribed_notifications.delay(upcoming_notification_time)
    return Response(data={"message": "Notification sent successfully."}, status=status.HTTP_200_OK)


@api_view(['POST'])
def update_cache(request):
    """
    Update cache for upcoming notifications.
    """
    update_cache_for_upcoming_notifications.delay()
    return Response(data={"message": "Cache update initiated."}, status=status.HTTP_200_OK)
