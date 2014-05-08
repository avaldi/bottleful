import unittest

import nose

from boapi.resources import BaseResource
from boapi.resources import register_resource


class TestBaseResource(unittest.TestCase):

    class FakeApplication(object):
        """ Fake application used to check the resources get properly registered
        """
        routes = []

        def route(self, path, method, *args, **kwargs):
            """ The route method is called everytime an endpoint must be
            registered. We just store the endpoint's information in an
            instance variable.
            """
            self.routes.append((method, path))

    def setUp(self):
        """ Setup operations.
        """
        self.application = self.FakeApplication()

    def test_resource_name_is_mandatory(self):
        """ Test that a resource without a resource_name cannot be instanciated
        """

        # Create a fake resource that simply subclass from BaseResource
        class FakeResourceWithoutName(BaseResource):
            pass

        # Try to register the resource. Asserts that a TypeError is raised
        # (we can't register the resource without defining a resource_name)
        nose.tools.assert_raises(
            TypeError,
            register_resource,
            self.application,
            FakeResourceWithoutName
        )

    def test_resource_registering(self):
        """ Test registering adds the expected routes to the application
        """

        # Fake resource with 2 endpoints (create and retrieve)
        class FakeResource(BaseResource):
            resource_name = 'test-resource'

            def create(self):
                pass

            def retrieve(self, resource_id):
                pass

        # We expect 2 endpoints to be registered with the proper HTTP methods
        # and URL
        expected_resources = [
            ('POST', '/test-resource'),
            ('GET', '/test-resource/<resource_id>'),
        ]

        register_resource(self.application, FakeResource)

        # Asserts that both endpoints have been registered
        for resource in expected_resources:
            nose.tools.assert_in(resource, self.application.routes)
