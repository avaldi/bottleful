

class BaseField(object):
    """
    """

    def __init__(self, field_type, field_format='', required=False,
                 primary_key=False):
        """
        """
        self.field_type = field_type
        self.field_format = field_format
        self.required = required
        self.primary_key = primary_key

    def as_dict(self):
        """
        """
        return {
            'type': self.field_type,
            'format': self.field_format,
        }


class BaseSchema(object):
    """
    """

    @classmethod
    def field_names(cls):
        for attr in dir(cls):
            if isinstance(getattr(cls, attr), BaseField):
                yield attr

    @classmethod
    def primary_key(cls):
        for attr in cls.field_names():
            if getattr(cls, attr).primary_key:
                return attr

    @classmethod
    def get_schema(cls):
        """
        """
        properties = {
            attr: getattr(cls, attr).as_dict() for attr in cls.field_names()
        }

        required_fields = [
            attr for attr in cls.field_names() if getattr(cls, attr).required
        ]

        return {
            'type': 'object',
            'properties': properties,
            'required': required_fields,
        }
