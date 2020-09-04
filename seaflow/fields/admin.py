from ..fields import ResponseField
from flask_restful.fields import Integer, Raw, List, Boolean, Nested

Lock_fields = {
    'uid': Integer,
    'lock': Boolean()
}

Locks_fields = {
    'users': List(Nested(Lock_fields))
}
LockRes = ResponseField(Locks_fields)
