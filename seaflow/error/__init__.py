from werkzeug.exceptions import HTTPException
from seaflow.fields import error_fields
from flask_restful import marshal
from itsdangerous import BadSignature, SignatureExpired


class ApiException(HTTPException):
    code = 500
    description = "deed"
    error_code = 500

    def __init__(self, description=None, code=None, error_code=None, *args, **kwargs):
        super(ApiException, self).__init__(description, *args, **kwargs)
        if code:
            self.code = code
        if error_code:
            self.error_code = error_code
        self.data = {"code": self.error_code, "message": self.description}


class CodeError(ApiException):
    code = 400
    description = '验证码错误'


class DbError(ApiException):
    code = 500
    description = "数据库错误"
    error_code = 40000


class NotFound(ApiException):
    code = 404
    description = "Not found"
    error_code = 404


class NotAllow(ApiException):
    code = 403
    description = "该资源不允许访问"
    error_code = 403


class NewsNotYours(ApiException):
    error_code = 30001
