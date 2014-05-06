import sys
import traceback

from bottle import HTTPError


class APIError(HTTPError):
    """ Main error exception. It subclass bottle.HTTPError automatically and
    adds the traceback to the response.
    """

    def __init__(self, *args, **kwargs):
        """ Attaches the traceback if it exists.
        """

        if sys.exc_info()[0]:
            kwargs['traceback'] = traceback.format_exc()

        super(APIError, self).__init__(*args, **kwargs)
