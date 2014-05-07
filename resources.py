import abc
import logging

import bottle

from boapi import HTTP_ACTIONS


logger = logging.getLogger(__name__)


class BaseResource(object):
    """ Base class to define restful resources.
    """

    __metaclass__ = abc.ABCMeta

    @abc.abstractproperty
    def resource_name(self):
        """ Resource name used to build the restful URLs.
        """
        raise NotImplementedError

    def __init__(self, application=bottle.default_app()):
        """ Initialize the restful resource. Basically registers the bottle
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
                    route_path = self.path_transformer(
                        action_properties['path'] % {
                            'resource_name': self.resource_name
                        }
                    )

                    logger.info(
                        'Registering route %s - %s',
                        method_name,
                        route_path
                    )

                    # register the bottle route
                    self.application.route(
                        path=route_path,
                        method=method_name,
                        callback=method
                    )

    def path_transformer(self, path):
        """ Helper function used to transform the route path before
        registering it. By default the method doesn't apply any transformation,
        subclass BaseResource and override the method to implement
        any transformation.
        """
        return path


class APIResource(BaseResource):
    """ Base API resource. Every resource should subclass from this class.
    """

    @abc.abstractproperty
    def resource_name(self):
        """ Resource name used to build the restful URLs.
        """
        raise NotImplementedError


def register_resource(application, resource_class):
    """ Register the bottle routes of a resource.
    """

    resource_class(application)
