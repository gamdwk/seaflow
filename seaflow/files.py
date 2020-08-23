from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from werkzeug.datastructures import FileStorage
from flask import current_app
import datetime
from os import makedirs
from os.path import join, splitext
import uuid

from .main.exts import auth
from .models.social import Files as FileModel


class Files(Resource):
    method_decorators = [auth.login_required()]

    def __init__(self):
        self.parser = RequestParser()
        self.parser.add_argument('files', type=list, location='files')
        self.parser.add_argument('type', type=str, chioce=['image', 'files'])

    def post(self):
        root = current_app.config['UPLOAD_PATH']
        file = FileModel()
        args = self.parser.parse_args()
        folder = args["type"]
        files = args["files"]

        for f in files:
            print(f.name)
            print(f.filename)
            dest, filename = create_filename(root, folder, f.filename)
            f.save(dest)
            file.init(name=f.name, path=join(dest, filename), type=folder)
        return


def create_filename(root, folder, filename):
    t = datetime.datetime.now().date()
    folder = folder + '/'
    try:
        makedirs(join(root, folder, str(t)))
    except FileExistsError:
        pass
    u = uuid.uuid4()
    suffix = get_suffix(filename)
    return join(folder, str(t)), str(u) + suffix


def get_suffix(filename):
    suffix = splitext(filename)[1]
    return suffix
