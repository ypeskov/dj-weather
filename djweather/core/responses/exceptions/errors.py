ERROR_CODES = {
    'INVALID_INPUT': (400, 'Invalid input'),
    'NOT_FOUND': (404, 'Not found'),

    'VALIDATION_ERROR': (400, 'Validation error'),

    'INTERNAL_SERVER_ERROR': (500, 'Internal server error'),

    'USER_ALREADY_EXISTS': (400, 'User already exists'),
    'PASSWORD_MISMATCH': (400, 'Passwords do not match'),
    'USER_REGISTRATION_ERROR': (400, 'User registration error'),

    'INVALID_CITY': (400, 'City is invalid. Please provide a valid city.'),

    'SUBSCRIPTION_ALREADY_EXISTS': (400, 'Subscription already exists'),
    'SUBSCRIPTION_DOES_NOT_EXIST': (400, 'Subscription does not exist'),

    'UNKNOWN_ERROR': (500, 'Unknown error'),
}
