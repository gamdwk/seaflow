from werkzeug.exceptions import HTTPException
from seaflow.fields import error_fields
from flask_restful import marshal
from itsdangerous import BadSignature, SignatureExpired


class ApiException(HTTPException):
    code = 500,
    description = "error"
    status = 500

    def __init__(self, description=None, code=None, status=None, *args, **kwargs):
        super().__init__(description, *args, **kwargs)
        if code:
            self.code = code
        if status:
            self.status = status


class CodeError(ApiException):
    code = 400
    description = '验证码错误'


class DbError(ApiException):
    code = 500
    description = "数据库错误"
    status = 500
