from . import ApiException


class UserNotExist(ApiException):
    code = 401
    description = "用户不存在"


class UserAlreadyExist(ApiException):
    code = 401
    description = "用户已经存在"


class PasswordError(ApiException):
    code = 401
    description = "密码错误"
