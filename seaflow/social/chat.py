from ..main.exts import io, auth, api, db
from flask_socketio import send, emit, Namespace, disconnect, rooms, join_room
from flask import request, g, session
from ..models.social import Messages
from ..helper.rediscli import is_alive, make_down, make_alive, set_sid, \
    delete_sid, get_uid
from ..fields.social import MessagesListRes, MessagesRes


class Chat(Namespace):

    @auth.login_required()
    def on_connect(self):
        uid = g.user["uid"]
        session["uid"] = uid
        set_sid(uid, request.sid)
        join_room(uid)
        make_alive(uid)
        send_messages(uid)

    @auth.login_required()
    def on_chat(self, data):
        uid = g.user["uid"]
        to = data["to"]
        content = data["content"]
        is_url = data["is_url"]
        m = Messages()
        m.init(uid, to, content, is_url=is_url)
        db.session.add(m)
        db.session.commit()
        res = m.make_fields()
        if is_alive(to):
            emit('chat', MessagesListRes.marshal({"messages": [res]}),
                 room=to,
                 callback=make_message_send([m]))
        emit('chat', MessagesListRes.marshal({"messages": [res]}))

    def on_disconnect(self):
        make_down(get_uid(request.sid))
        delete_sid(request.sid)


def send_messages(uid):
    msgs = Messages.query.filter_by(to_user=uid, is_send=False).filter(
        Messages.agree.is_(None)
    ).all()
    if len(msgs) == 0:
        return
    res = []
    for msg in msgs:
        re = msg.make_fields()
        res.append(re)
    emit('chat', MessagesListRes.marshal({"messages": res}),
         callback=make_message_send(msgs))


def make_message_send(msglist):
    for msg in msglist:
        msg.is_send = True
    db.session.commit()
