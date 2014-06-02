import logging
import httplib

import jsonschema

from bottle import request
from bottle import response

from bottleful.errors import APIError


logger = logging.getLogger(__name__)


class BaseView(object):
    """ Base view class. Subclasses must define a render method that will
    be called every time the view is requested by the client.
    """

    def __call__(self, *args, **kwargs):
        """ Main method of the view. It defines the overall flow of the view.
        """
        # compute the response
        api_response = self.render(*args, **kwargs)
        # transform the response to a dict
        dict_response = api_response.as_dict()
        # set the bottle response status code and return the response as a dict
        response.status = api_response.status_code

        return dict_response

    def render(self, *args, **kwargs):
        """ Render method that defines the logic of the view.
        It must be overridden by the subclasses and must return an
        APIResponse object including the response to be sent to the client.
        """
        raise NotImplementedError


class ValidatedJsonView(BaseView):
    """ View that provides json validation before rendering the response.
    Subclasses must implement the schema method to return a schema class to
    be used when performing the validation through the jsonschema library.
    """

    def schema(self, *args, **kwargs):
        """ Placeholder to raise an Exception if the subclass does not implement
        the schema method.
        """
        raise NotImplementedError

    def _validate_request(self, *args, **kwargs):
        """ Validate the body of the request coming from the client based
        on the provided schema (returned by the .schema() mnethod).
        """

        # try to parse the JSON data sent by the client
        try:
            request_json = request.json
        except ValueError:
            request_json = None

        # if we can't make it, raise a 400
        if not request_json:
            raise APIError(httplib.BAD_REQUEST, 'Request is not JSON')

        # Get the schema from the the subclass implementing schema()
        schema = self.schema(*args, **kwargs)

        if not schema:
            # If we don't have a schema, just returns. We basically only
            # check that the request has valid Json format.
            return

        # Validates the json content of the request using jsonschema library,
        # according to the schema provided
        try:
            jsonschema.validate(
                request_json,
                schema.as_json_schema(),
                format_checker=jsonschema.FormatChecker()
            )
        except jsonschema.ValidationError as e:
            logger.exception('Schema validation error')

            raise APIError(
                httplib.BAD_REQUEST,
                'Schema validation error: %s' % e.message,
                exception=e
            )

    def __call__(self, *args, **kwargs):
        """ Main method of the view. It overrides the main flow of the BaseView
        by adding the validation process.
        """

        # validate the request
        self._validate_request(*args, **kwargs)
        # call the super to handle the response
        return super(ValidatedJsonView, self).__call__(*args, **kwargs)
