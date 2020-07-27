from . import ApiException


class UserNotExist(ApiException):
    code = 404
    description = "用户不存在"
    error_code = 10000


class UserAlreadyExist(ApiException):
    code = 401
    description = "用户已经存在"
    error_code = 10001


class PasswordError(ApiException):
    code = 401
    description = "密码错误"
    error_code = 10002


class AuthException(ApiException):
    code = 404
    error_code = 10003
    description = "错误"
