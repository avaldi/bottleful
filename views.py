import logging
import traceback
import requests

import jsonschema
from bottle import HTTPError
from bottle import request
from bottle import response


logger = logging.getLogger(__name__)


class BaseView(object):
    """
    """

    def __call__(self, *args, **kwargs):
        """
        """
        # compute the response
        api_response = self.render(*args, **kwargs)
        # transform the response to a dict
        dict_response = api_response.as_dict()
        # set the bottle response status code and return the response as a dict
        response.status = api_response.status_code
        return dict_response

    def render(self, *args, **kwargs):
        """
        """
        raise NotImplementedError


class ValidatedJsonView(BaseView):
    """
    """

    def get_schema(self, *args, **kwargs):
        """ TODO: change the schema for proper validation
        """
        return {}

    def _validate_request(self, *args, **kwargs):
        """
        """
        # try to parse the JSON data sent by the client
        try:
            request_json = request.json
        except ValueError:
            request_json = None

        # if we can't make it, raise a 400
        if not request_json:
            raise HTTPError(requests.codes.bad, 'Request is not JSON')

        try:
            jsonschema.validate(
                request_json,
                self.get_schema(*args, **kwargs),
                format_checker=jsonschema.FormatChecker()
            )
        except jsonschema.ValidationError as e:
            logger.exception('Schema validation error')
            raise HTTPError(
                requests.codes.bad,
                'Schema validation error: %s',
                exception=e,
                traceback=traceback.format_exc()
            )

    def __call__(self, *args, **kwargs):
        # validate the request
        self._validate_request(*args, **kwargs)
        # call the super to handle the response
        return super(ValidatedJsonView, self).__call__(*args, **kwargs)
