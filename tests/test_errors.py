import unittest

import nose

from bottleful.errors import APIError


class TestAPIError(unittest.TestCase):
    """ Test APIError functionality
    """

    def test_traceback_is_added(self):
        """ Test that the exception traceback gets added to the response
        """

        exception_message = 'Test exception'

        try:
            raise Exception(exception_message)
        except Exception:
            try:
                raise APIError(404, 'API error')
            except APIError as exc:
                nose.tools.assert_in(exception_message, exc.traceback)
