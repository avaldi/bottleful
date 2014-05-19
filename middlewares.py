

class StripPathMiddleware(object):
    """ Middleware to strip out slashes from URLs.
    Shamelessly stolen from:
      http://bottlepy.org/docs/dev/recipes.html#ignore-trailing-slashes
    """

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        """ Remove all the trailing slashes from the requested URL
        """
        environ['PATH_INFO'] = environ['PATH_INFO'].rstrip('/')
        return self.app(environ, start_response)
