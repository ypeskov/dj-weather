from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny

from icecream import ic

from .serializers import UserRegistrationSerializer, UserInfoSerializer
from core.responses.successes.successes import ApiSuccessResponse


@permission_classes([AllowAny])
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


@api_view(['GET'])
def get_user_info(request):
    user = request.user

    serializer = UserInfoSerializer(user)
    data, status_code = ApiSuccessResponse(
        response_code='SUCCESS',
        status_code=status.HTTP_200_OK,
        message="User information retrieved successfully.",
        details=serializer.data
    ).to_response()

    return Response(data=data, status=status_code)
