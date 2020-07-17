from flask_restful import Api, Resource, abort
from flask import Flask, session
from config import DevelopmentConfig
from werkzeug.exceptions import HTTPException
from flask_restful import marshal
from flask_restful.fields import Integer, Nested, String

app = Flask(__name__)
api = Api(app, catch_all_404s=True, errors={
    'UserAlreadyExistsError': {
        'message': "A user with that username already exists.",
        'code': 200,
    },
    'ResourceDoesNotExist': {
        'message': "A resource with that ID no longer exists.",
        'code': 410,
        'extra': "Any extra information you want.",
    },
})
app.config.from_object(DevelopmentConfig)

def a(*args):
    b(*args)

def b(c,d):
    print(c)
    print(d)

a(1,5)

class UserAlreadyExistsError(HTTPException):
    code = 500
    description = "user"


class ErrorTest(Resource):
    def get(self):
        raise UserAlreadyExistsError

    def post(self):
        return


api.add_resource(ErrorTest, '/')


class dictObj(object):
    def __init__(self):
        self.x = 'red'
        self.y = 'Yellow'
        self.z = 'Green'

    def do_nothing(self):
        pass


test = dictObj()
print(test.__dict__)