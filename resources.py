import abc
import logging

import bottle

from boapi import HTTP_ACTIONS


logger = logging.getLogger(__name__)


class BaseResource(object):
    """ Base class to define Restful resources.
    """

    __metaclass__ = abc.ABCMeta

    @abc.abstractproperty
    def resource_name(self):
        """ Resource name used to build the Restful URLs.
        """
        raise NotImplementedError

    def __init__(self, application=bottle.default_app()):
        """ Initialize the Restful resource. Basically registers the bottle
            routes for all the defined methods in the resource.
        """

        self.application = application

        for action, action_properties in HTTP_ACTIONS.iteritems():
            method_name = action_properties['method']
            try:
                method = getattr(self, action)
            except AttributeError:
                pass
            else:
                if callable(method):
                    route_path = action_properties['path'] % {
                        'resource_name': self.resource_name
                    }

                    route_path = self.path_transformer(route_path)

                    logger.info(
                        'Registering route %s - %s',
                        method_name,
                        route_path
                    )

                    # Register bottle route
                    self.application.route(
                        route_path,
                        method=method_name,
                        callback=method
                    )

    def path_transformer(self, url):
        return url


class ApiResource(BaseResource):
    """
    """
    pass


class CountryBasedApiResource(BaseResource):
    def path_transformer(self, path):
        country_path_format = '/countries/<country_id:int>'

        return country_path_format +  path


def register_resource(application, resource_class):
    """ Register the bottle routes of a resource.
    """
    resource_class(application)
