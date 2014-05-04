import logging

import requests

import jsonschema

from bottle import HTTPError
from bottle import request


logger = logging.getLogger(__name__)


class BaseView(object):

    def render(self):
        raise NotImplementedError

    def __call__(self, *args, **kwargs):
        response = self.render()
        return response.as_dict()


class ValidatedJsonView(BaseView):

    # TODO: make it abstract attribute
    schema = {}

    def _validate_request(self):
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
        self._validate_request()
        return super(ValidatedJsonView, self).__call__(*args, **kwargs)
