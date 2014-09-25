__author__ = 'Joe Linn'


class APIError(Exception):
        def __init__(self, msg, code=None):
            self.msg = msg
            self.code = code
            Exception.__init__(self, msg, code)

        def __str__(self):
            return '{0} - {1}'.format(self.code, self.msg) if self.code is not None else self.msg

from .client import PyflareClient
from .hosting import PyflareHosting

Pyflare = PyflareClient
