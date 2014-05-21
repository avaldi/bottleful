import sys
import traceback as tb

from bottle import HTTPError


class APIError(HTTPError):
    """ Main error exception. It subclass bottle.HTTPError automatically and
    adds the traceback to the response.
    """

    def __init__(self, status=None, body=None, exception=None, traceback=None,
                 **options):
        """ Attaches the traceback if it exists.
        """

        if sys.exc_info()[0]:
            traceback = tb.format_exc()

        super(APIError, self).__init__(
            status=status,
            body=body,
            exception=exception,
            traceback=traceback,
            **options
        )
