import unittest

import nose

from bottleful.response import APIResponse


class TestAPIResponse(unittest.TestCase):
    """ Test APIResponse functionality
    """

    def setUp(self):
        """ Setup operations.
        """
        self.response_data = {
            'information': 'bla-bla'
        }

        self.expected_response = {
            'success': False,
            'data': self.response_data.copy()
        }


    def test_invalid_status_code(self):
        """ Test APIResponse behavior with invalid status codes
        """

        invalid_status_codes = ['random_string', 1200]

        # Try to assign the invalid status codes and assert that a ValueError
        # exception is raised
        for status_code in invalid_status_codes:
            nose.tools.assert_raises(
                ValueError,
                APIResponse,
                status_code
            )

    def test_bad_status_codes(self):
        """ Test the response dictionary when setting a bad status code
        """

        self.expected_response['success'] = False

        # Test the response with a 404 - Not Found status code
        self._test_response(404, self.response_data, self.expected_response)

    def test_good_status_codes(self):
        """ Test the response dictionary when setting a good status code
        """

        self.expected_response['success'] = True

        # Test the response with a 204 - No Content status code
        self._test_response(204, self.response_data, self.expected_response)

    @staticmethod
    def _test_response(status_code, response_data, expected_dict):
        """ Helper function to test the APIResponse dictionary based on the
        status code and the response data.
        """

        api_response = APIResponse(
            status_code=status_code,
            **response_data
        )

        # Transform the response to a dictionary
        response = api_response.as_dict()

        # Assert the response dictionary is what we expected
        nose.tools.assert_equals(response, expected_dict)
