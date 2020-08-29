from . import ResponseField
from flask_restful.fields import Integer, Nested, Url, String, Raw, Boolean, DateTime, List
from flask_restful import marshal

newsfield = {
    'content': String(),
    'imgs': List(String()),
    'time': DateTime(dt_format='iso8601'),
    'uid': Integer,
    'tid': Integer,
    'liked': Boolean,
    'likes': Integer,
    "comments": Integer,
    "avatar": String,
    "sex": Integer,
    "username": String
}

createnewsfield = {
    'uid': Integer,
    'tid': Integer
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

commentsField = {
    'content': String(),
    'imgs': List(String),
    'time': DateTime(dt_format='iso8601'),
    'uid': Integer,
    'tid': Integer,
    "cid": Integer,
    'liked': Boolean(default=False),
    'likes': Integer,
    'parent': Integer,
    "ancestor": Integer,
    "avatar": String,
    "sex": Integer,
    "username": String
}
replycomments = commentsField.copy()
replycomments["parentUID"] = Integer
GroupField = {
    "gid": Integer,
    "ancestor": Nested(commentsField),
    "members": List(Nested(replycomments)),
    "pages": Integer,
    "current": Integer
}

replyField = GroupField
commentList = {
    "groups": List(Nested(GroupField))
}
replyListField = {
    'replies': List(Nested(replyField)),
    "current": Integer,
    "pages": Integer
}

fileField = {
    "filename": String,
    "path": String,
    "fid": Integer
}
fileListField = {
    "files": List(Nested(fileField))
}

messagesFields = {
    "mid": Integer,
    "from": Integer,
    "to": Integer,
    "content": String,
    "type": String,
    "is_url": Boolean,
    "time": DateTime(dt_format='iso8601'),
    "agree": Boolean
}
messageList = {
    "messages": List(Nested(messagesFields)),
}

friendsReplyList = {
    "reply": List(Nested(messagesFields))
}
createnewsRes = ResponseField(createnewsfield)
newsRes = ResponseField(newsfield)
newslistRes = ResponseField(newslist)
newslikeRes = ResponseField(newslike)
commentRes = ResponseField(commentsField)
commentListRes = ResponseField(commentList)
fileRes = ResponseField(fileListField)
GroupRes = ResponseField(GroupField)
RepliesRes = ResponseField(replyListField)
MessagesRes = ResponseField(messagesFields)
MessagesListRes = ResponseField(messageList)
friendsReply = ResponseField(friendsReplyList)
