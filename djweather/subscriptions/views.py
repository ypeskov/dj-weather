from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from icecream import ic

from core.responses.exceptions.exceptions import ApiException
from core.responses.successes.successes import ApiSuccessResponse
from .serializers import SubscriptionSerializer


class SubscriptionView(APIView):
    def post(self, request):
        serializer = SubscriptionSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            try:
                serializer.save()
                data, status_code = ApiSuccessResponse(
                    message="Subscription created successfully.",
                    details=serializer.data
                ).to_response()
                return Response(data=data, status=status_code)
            except ApiException as e:
                if isinstance(e, ApiException):
                    # log exception
                    ic(e)

                raise ApiException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    error_code='INTERNAL_SERVER_ERROR',
                    message="Error while creating subscription. Please try again later."
                )
