from .auth import *
from flask_restful.fields import Integer, String

error_fields = {
    "code": Integer(default=404),
    "message": String(default="Not Found Resource")
}
common_response = ResponseField()
