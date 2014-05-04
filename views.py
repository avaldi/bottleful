import logging

import requests

import jsonschema

from bottle import HTTPError
from bottle import request
from bottle import response


logger = logging.getLogger(__name__)


class BaseView(object):

    def __call__(self, *args, **kwargs):
        # Compute the response
        api_response = self.render(*args, **kwargs)
        # Transform the response to a dict
        dict_response = api_response.as_dict()
        # Set the bottle response status code and return the response as a dict
        response.status = api_response.status_code
        return dict_response

    def render(self):
        raise NotImplementedError


class ValidatedJsonView(BaseView):

    # TODO: make it abstract attribute
    schema = {}

    def before_validation(self, *args, **kwargs):
        pass

    def after_validation(self, *args, **kwargs):
        pass

    def _validate_request(self, *args, **kwargs):
        # Try to parse the Json data sent by the client
        try:
            request_json = request.json
        except ValueError:
            request_json = None

        # If we can't make it, raise a 400
        if not request_json:
            raise HTTPError(requests.codes.bad, 'Request is not JSON')

        try:
            jsonschema.validate(
                request_json,
                self.schema,
                format_checker=jsonschema.FormatChecker()
            )
        except jsonschema.ValidationError:
            logger.exception('Schema validation error')
            raise HTTPError(requests.codes.bad, 'Schema validation error')

    def __call__(self, *args, **kwargs):

        self.before_validation(*args, **kwargs)
        # Validate the request
        self._validate_request(*args, **kwargs)
        self.after_validation(*args, **kwargs)

        # Call super to handle the response
        return super(ValidatedJsonView, self).__call__(*args, **kwargs)
