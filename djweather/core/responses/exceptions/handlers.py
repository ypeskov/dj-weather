from rest_framework.views import exception_handler
from rest_framework.response import Response

from .exceptions import ApiException
from .errors import ERROR_CODES


def api_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, ApiException):
        status_code, message = ERROR_CODES[exc.error_code]
        if exc.status_code:
            status_code = exc.status_code
        if exc.message:
            message = exc.message

        data = {
            'error_code': exc.error_code,
            'message': message,
            'details': exc.details,
        }
        response = Response(data, status=status_code)

    return response
