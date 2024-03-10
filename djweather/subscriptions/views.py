import json

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from icecream import ic

from core.responses.exceptions.exceptions import ApiException
from core.responses.successes.successes import ApiSuccessResponse
from .serializers import SubscriptionSerializer, UnsubscriptionSerializer
from .services import subscribe_user_to_weather_updates, unsubscribe_user_to_weather_updates
from .tasks import send_email


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


@api_view(['POST'])
def send_notification(request):
    """
    This is TEST endpoint for sending notification to user for the subscribed city.
    Send notification to user for the subscribed city.
    """
    weather = """
{
  "data": {
    "time": "2024-03-10T18:17:00Z",
    "values": {
      "cloudBase": 0.16,
      "cloudCeiling": 0.16,
      "cloudCover": 55,
      "dewPoint": 23.31,
      "freezingRainIntensity": 0,
      "humidity": 93,
      "precipitationProbability": 0,
      "pressureSurfaceLevel": 990.98,
      "rainIntensity": 0,
      "sleetIntensity": 0,
      "snowIntensity": 0,
      "temperature": 24.5,
      "temperatureApparent": 24.5,
      "uvHealthConcern": 0,
      "uvIndex": 0,
      "visibility": 16,
      "weatherCode": 1101,
      "windDirection": 132.81,
      "windGust": 1.81,
      "windSpeed": 0.88
    }
  },
  "location": {
    "lat": -15.253840446472168,
    "lon": 48.25621795654297,
    "name": "Sofia, Province de Mahajanga, Madagasikara / Madagascar",
    "type": "state"
  }
}
    """
    weather_json = json.loads(weather)
    send_email.delay(request.user.id, weather_json)
    return Response(data={"message": "Notification sent successfully."}, status=status.HTTP_200_OK)
