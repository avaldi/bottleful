

DEFAULT_SUCCESS_DICT = {
    'data': {},
    'success': True
}

DEFAULT_FAILURE_DICT = {
    'data': {},
    'success': False
}


class APIResponse(object):
    """ Basic JSON response to be sent by the API
    """

    response_format = None

    def __init__(self, status_code=200, **kwargs):
        """ Instantiate an APIResponse object setting the passed status code
            and adding every keyword argument to the response.
        """
        if not (100 <= status_code < 600):
            raise ValueError('Invalid status code')

        self.status_code = status_code
        self.result_data = kwargs.copy()

    def as_dict(self):
        """ Generate a dictionary containing the response to be returned
            to the client depending on the set status code.
        """

        # If the status code is bad (4xx and 5xx) use the default_failure_dict
        # otherwise default_success_dict
        if 400 <= self.status_code < 600:
            self.response_format = DEFAULT_FAILURE_DICT
        else:
            self.response_format = DEFAULT_SUCCESS_DICT

        result = self.response_format.copy()

        # Set the data field to contain the keyword argumentss passed
        # when the object was initialized
        result['data'] = self.result_data

        return result
