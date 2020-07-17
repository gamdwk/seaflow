from redis import StrictRedis, ConnectionPool
from datetime import timedelta
pool = ConnectionPool(host='localhost', port=6379, db=1, decode_responses=True)
cli = StrictRedis(connection_pool=pool)


def save_check_code(email, code):
    cli.set(email, code, ex=timedelta(minutes=5))


def verify_code(email, code):
    e_code = cli.get(email)
    return e_code == code
