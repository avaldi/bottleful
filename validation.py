

class BaseField(object):
    """
    """

    def __init__(self, field_type, field_format='', required=False):
        """
        """
        self.field_type = field_type
        self.field_format = field_format
        self.required = required

    def as_dict(self):
        """
        """
        return {
            'type': self.field_type,
            'format': self.field_format
        }


class BaseSchema(object):
    """
    """

    @classmethod
    def get_schema(cls):
        """
        """

        field_names = [
            attr for attr in dir(cls) if isinstance(getattr(cls, attr),
                                                    BaseField)
        ]

        properties = {
            attr: getattr(cls, attr).as_dict() for attr in field_names
        }

        required_fields = [
            attr for attr in field_names if getattr(cls, attr).required
        ]

        return {
            'type': 'object',
            'properties': properties,
            'required': required_fields
        }
