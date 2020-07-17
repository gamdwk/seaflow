from flask_restful.fields import Integer, Nested, Url, String, Raw, Boolean
from flask_restful import marshal


class ResponseField(dict):

    def __init__(self, data_field, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self["code"] = Integer(default=0)
        self["message"] = String(default="success")
        self["data"] = Nested(data_field)

    def marshal(self, data=None, code=None, message=None):
        data = {"data": data, "code": code,
                "message": message}
        return marshal(data, self)


auth_field = {
    'access_token': String,
    'refresh_token': String
}

user_field = {
    "email": String,
    "sex": Integer,
    "introduction": String,
    "lock": Boolean,
    "pageBgc": String,
    "avatar": String
}

email_field = {
    'email': String
}
auth_response = ResponseField(auth_field)
user_response = ResponseField(user_field)
email_response = ResponseField(email_field)

