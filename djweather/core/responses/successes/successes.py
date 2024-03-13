import json


class ApiSuccessResponse:
    def __init__(self, response_code='SUCCESS', status_code=200, message=None, details=None):
        self.status_code = status_code
        self.response_code = response_code
        self.message = message
        self.details = details or []

    def to_response(self):
        return {
            'response_code': self.response_code,
            'message': self.message,
            'details': self.details,
        }, self.status_code
