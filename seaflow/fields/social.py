from . import ResponseField
from flask_restful.fields import Integer, Nested, Url, String, Raw, Boolean, DateTime, List

newsfield = {
    'content': String(),
    'imgs': List(String),
    'time': DateTime(dt_format='iso8601'),
    'uid': Integer
}

createnewsfield = {
    'uid': Integer,
    'tid': Integer
}

createnewsRes = ResponseField(createnewsfield)
newsRes = ResponseField(newsfield)
