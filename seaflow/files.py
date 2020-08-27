from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from werkzeug.datastructures import FileStorage
from flask import current_app
import datetime
from os import makedirs
from os.path import join, splitext
import uuid

from .main.exts import auth, db, api
from .models.social import Files as FileModel
from .fields.social import fileRes


class Files(Resource):
    method_decorators = [auth.login_required()]

    def __init__(self):
        self.parser = RequestParser()
        self.parser.add_argument('files', type=FileStorage, location='files', action="append")
        self.parser.add_argument('images', type=FileStorage, location='files', action="append")

    def get(self, id):
        return

    def post(self):
        root = current_app.config['UPLOAD_PATH']
        args = self.parser.parse_args()
        files = args["files"]
        images = args["images"]
        filelist = []
        if files and images:
            fs = files
            fs.extend(images)
        else:
            fs = files or images
        for f in fs:
            file = FileModel()
            folder = f.name
            dest, filename = create_filename(root, folder, f.filename)
            f.save(join(root, dest, filename))
            f.close()
            file.init(name=f.filename, path=join(dest, filename), type=folder)
            try:
                db.session.add(file)
                db.session.commit()
                filelist.append({"filename": file.name, "path": file.path, "fid": file.id})
            except:
                filelist.append({"filename": file.name, "error": "数据库错误"})

        return fileRes.marshal({"files": filelist})


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


api.add_resource(Files, '/files', '/files/<int:id>')
