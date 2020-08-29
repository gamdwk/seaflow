from redis import StrictRedis, ConnectionPool
from datetime import timedelta
from .secret import create_salt

pool = ConnectionPool(host='localhost', port=6379, db=1, decode_responses=True)


def save_check_code(email, code):
    cli = StrictRedis(connection_pool=pool)
    cli.set(email, code, ex=timedelta(minutes=5))


def verify_code(email, code):
    cli = StrictRedis(connection_pool=pool)
    e_code = cli.get(email)
    if e_code == code:
        cli.delete(email)
        return True
    else:
        return False


def save_salt(uid):
    salt = create_salt()
    cli = StrictRedis(connection_pool=pool)
    cli.set(uid, salt)


def get_salt(uid):
    cli = StrictRedis(connection_pool=pool)
    return cli.get(uid)


type_tuple = ("news", "comments")


# news_like:hash,tid_or_cid:news_likes
def like_news(uid, tid_or_cid, t=0):
    t = type_tuple[t]
    cli = StrictRedis(connection_pool=pool)
    myset = t + str(tid_or_cid)
    t = t + '_likes'
    cli.hsetnx(t, tid_or_cid, 0)
    if cli.sismember(myset, uid):
        cli.hincrby(t, tid_or_cid, -1)
        cli.srem(myset, uid)
    else:
        cli.hincrby(t, tid_or_cid)
        cli.sadd(myset, uid)


def news_is_like(uid, tid_or_cid, t=0):
    # t= "news" or "comments"
    t = type_tuple[t]
    cli = StrictRedis(connection_pool=pool)
    myset = t + str(tid_or_cid)
    return cli.sismember(myset, uid)


def get_like(tid_or_cid, t=0):
    t = type_tuple[t]
    cli = StrictRedis(connection_pool=pool)
    myset = t + "_likes"
    x = cli.hget(myset, tid_or_cid) or 0
    return x


def get_sid(uid):
    cli = StrictRedis(connection_pool=pool)
    return cli.hget("user_sid", uid)


def set_sid(uid, sid):
    cli = StrictRedis(connection_pool=pool)
    cli.hset("user_sid", uid, sid)


def delete_sid(uid):
    cli = StrictRedis(connection_pool=pool)
    cli.hdel("user_sid", uid)


def is_alive(uid):
    cli = StrictRedis(connection_pool=pool)
    return cli.hget("is_alive", uid) or False


def make_alive(uid):
    cli = StrictRedis(connection_pool=pool)
    cli.hset("is_alive", uid, 1)


def make_down(uid):
    cli = StrictRedis(connection_pool=pool)
    cli.hset("is_alive", uid, 0)
