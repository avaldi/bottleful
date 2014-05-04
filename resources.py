from boapi.base import BaseResource


class ApiResource(BaseResource):
    """
    """
    pass


def register_resource(application, resource_class):
    """ Register the bottle routes of a resource.
    """
    resource_class(application)
