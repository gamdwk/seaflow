from .auth import *
from flask_restful.fields import Integer, String
import os
error_fields = {
    "code": Integer(default=404),
    "message": String(default="Not Found Resource")
}
common_response = ResponseField()


class StaticUrl(Raw):

    def format(self, value):
        return 'http://39.97.113.252:8080/static/' + value
