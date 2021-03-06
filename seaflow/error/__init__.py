from werkzeug.exceptions import HTTPException
from seaflow.fields import error_fields
from flask_restful import marshal
from itsdangerous import BadSignature, SignatureExpired
from werkzeug.datastructures import Headers
from flask import request


class ApiException(HTTPException):
    code = 500
    description = "error"
    error_code = 500

    def __init__(self, description=None, code=None, error_code=None, *args, **kwargs):
        super(ApiException, self).__init__(description, *args, **kwargs)
        if code:
            self.code = code
        if error_code:
            self.error_code = error_code
        self.data = {"code": self.error_code, "message": self.description}

    def get_headers(self, environ=None):

        headers = Headers([("Content-Type", "application/json; charset=utf-8")])
        if 'Origin' in request.headers:
            origin = request.headers['Origin']
            headers.update(
                {'Access-Control-Allow-Origin': origin, 'Access-Control-Allow-Method': 'OPTIONS,HEAD,GET,POST'
                    , 'Access-Control-Allow-Headers': '*', 'Access-Control-Allow-Credentials': 'true',
                 'Vary': 'Origin'})
        return headers


class CodeError(ApiException):
    code = 400
    description = 'VerificationCodeError '


class DbError(ApiException):
    code = 500
    description = "DatabaseError"
    error_code = 40000


class NotFound(ApiException):
    code = 404
    description = "Not found"
    error_code = 404


class NotAllow(ApiException):
    code = 403
    description = "Not Allow"
    error_code = 403


class NewsNotYours(ApiException):
    error_code = 30001
