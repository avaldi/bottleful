import traceback
import sys

from bottle import HTTPError


class APIError(HTTPError):
    """ Main error exception. It subclass bottle.HTTPError automatically
        adding the traceback to the response.
    """

    def __init__(self, *args, **kwargs):

        if sys.exc_info()[0]:
            kwargs['traceback'] = traceback.format_exc()

        super(APIError, self).__init__(*args, **kwargs)
