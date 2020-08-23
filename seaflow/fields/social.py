from . import ResponseField
from flask_restful.fields import Integer, Nested, Url, String, Raw, Boolean, DateTime, List

newsfield = {
    'content': String(),
    'imgs': List(String),
    'time': DateTime(dt_format='iso8601'),
    'uid': Integer,
    'tid': Integer
}

createnewsfield = {
    'uid': Integer,
    'tid': Integer
}

newslistfield = {

}
newslist = {
    "news": []
}

newslike = {
    'tid': Integer,
    'uid': Integer,
    'likes': Integer,
    'liked': Boolean(default=False)
}

createnewsRes = ResponseField(createnewsfield)
newsRes = ResponseField(newsfield)
newslistRes = ResponseField(newslist)
newslikeRes = ResponseField(newslike)
