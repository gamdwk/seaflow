from flask_restful.fields import Integer, Nested, Url, String, Raw, Boolean, List
from flask_restful import marshal


class ResponseField(dict):

    def __init__(self, data_field=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self["code"] = Integer(default=0)
        self["message"] = String(default="success")
        self["data"] = Nested(data_field, default={})

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
    "avatar": String,
    "username": String
}
user_register_field = {
    "email": String,
    "uid": Integer
}
email_field = {
    'email': String
}

friends = {
    "friends": List(Integer),
    "current": Integer,
    "pages": Integer
}
UserList = {
    "users": List(Nested(user_field)),
    "current": Integer,
    "pages": Integer
}
auth_response = ResponseField(auth_field)
user_response = ResponseField(user_field)
email_response = ResponseField(email_field)
user_register_response = ResponseField(user_register_field)
friendsRes = ResponseField(friends)
userListRes = ResponseField(UserList)
