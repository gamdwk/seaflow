from werkzeug.exceptions import HTTPException
from itsdangerous import BadSignature, SignatureExpired
from ..auth.fields import auth_field
from flask_restful import marshal


class ApiException(HTTPException):
    code = None,
    description = None

    def __init__(self, description=None, code=None, *args, **kwargs):
        super().__init__(description, *args, **kwargs)
        if code is None:
            code = self.code
        self.code = code


class CodeError(ApiException):
    code = 400
    description = '验证码错误'


errors = {
    "BadSignature": marshal({}, auth_field),
    "SignatureExpired": marshal({}, auth_field)
}
