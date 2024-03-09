from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from icecream import ic

from core.responses.exceptions.exceptions import ApiException
from core.responses.successes.successes import ApiSuccessResponse
from .serializers import SubscriptionSerializer, UnsubscriptionSerializer
from .services import subscribe_user_to_weather_updates, unsubscribe_user_to_weather_updates


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

