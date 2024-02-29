class ApiException(Exception):
    def __init__(self, error_code='UNKNOWN_ERROR', status_code=500, message=None, details=None):
        super().__init__(message)
        self.status_code = status_code
        self.error_code = error_code
        self.message = message
        self.details = details or []

