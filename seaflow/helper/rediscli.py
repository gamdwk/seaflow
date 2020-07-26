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

