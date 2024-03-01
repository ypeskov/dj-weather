from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import UserRegistrationSerializer
from core.responses.successes.successes import ApiSuccessResponse


class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            data, status_code = ApiSuccessResponse(
                status_code=status.HTTP_201_CREATED,
                message="User created successfully.",
                details=UserRegistrationSerializer(user).data
            ).to_response()
            return Response(data=data, status=status_code)
