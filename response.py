
default_success_dict = {
    'data': {},
    'success': True
}


default_failure_dict = {
    'data': {},
    'success': False
}


class ApiResponse(object):
    """ Basic JSON response to be sent by the API
    """

    def __init__(self, status_code=200, **kwargs):
        self.status_code = status_code
        self.result_data = kwargs.copy()

    def as_dict(self):
        """
        """

        if 400 <= self.status_code < 600:
            self.response_format = default_failure_dict
        else:
            self.response_format = default_success_dict

        result = self.response_format.copy()
        result['data'] = self.result_data

        return result
