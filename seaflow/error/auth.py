from . import ApiException


class UserNotExist(ApiException):
    code = 404
    description = "User not exist"
    error_code = 10000


class UserAlreadyExist(ApiException):
    code = 401
    description = "User already exist"
    error_code = 10001


class PasswordError(ApiException):
    code = 401
    description = "PasswordError"
    error_code = 10002


class AuthException(ApiException):
    code = 404
    error_code = 10003
    description = "AuthError"
