import logging
import traceback
import requests

import jsonschema

from bottle import request
from bottle import response

from boapi.errors import ApiError


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


class SchemaAwareView(BaseView):

    def schema(self, *args, **kwargs):
        """ TODO: change the schema for proper validation
        """
        raise NotImplementedError


class ValidatedJsonView(SchemaAwareView):
    """
    """

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
            raise ApiError(requests.codes.bad, 'Request is not JSON')

        try:
            jsonschema.validate(
                request_json,
                self.schema(*args, **kwargs).as_json_schema(),
                format_checker=jsonschema.FormatChecker()
            )
        except jsonschema.ValidationError as e:
            logger.exception('Schema validation error')
            raise ApiError(
                requests.codes.bad,
                'Schema validation error',
                exception=e,
                traceback=traceback.format_exc()
            )

    def __call__(self, *args, **kwargs):
        # validate the request
        self._validate_request(*args, **kwargs)
        # call the super to handle the response
        return super(ValidatedJsonView, self).__call__(*args, **kwargs)
