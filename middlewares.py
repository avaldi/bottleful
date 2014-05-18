

class StripPathMiddleware(object):
    """ Middleware to strip out slashes from URLs
    """

    def __init__(self, app):
        self.app = app

    def __call__(self, e, h):
        """ Remove all the trailing slashes from the requested URL
        """
        e['PATH_INFO'] = e['PATH_INFO'].rstrip('/')
        return self.app(e,h)
