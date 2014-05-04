
default_success_dict = {
    'data': {},
    'success': True
}


default_failure_dict = {
    'data': {},
    'success': False
}


class BaseApiResponse(object):
    """ Basic JSON response to be sent by the API
    """

    def __init__(self, **kwargs):
        self.result_data = kwargs.copy()

    def as_dict(self):
        """
        """
        res = self.response_format.copy()
        res['data'] = self.result_data

        return res


class ApiResponse(BaseApiResponse):

    response_format = default_success_dict


class FailureApiResponse(BaseApiResponse):

    response_format = default_failure_dict
