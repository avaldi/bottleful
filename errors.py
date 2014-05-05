import traceback
import sys

from bottle import HTTPError


class APIError(HTTPError):

    def __init__(self, *args, **kwargs):

        if sys.exc_info()[0]:
            kwargs['traceback'] = traceback.format_exc()

        super(APIError, self).__init__(*args, **kwargs)
