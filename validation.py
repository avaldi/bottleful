

class BaseField(object):
    type = None
    format = None

    def __init__(self, field_type, field_format=None, required=False):
        """
        """
        self.type = field_type
        self.format = field_format
        self.required = required

    def as_dict(self):
        """
        """
        return {
            'type': self.type,
            'format': self.format or ''
        }


class BaseSchema(object):

    def generate_schema(self):
        """
        """

        field_names = [
            attr for attr in dir(self) if isinstance(getattr(self, attr),
                                                     BaseField)
        ]

        properties = dict([
            (attr, getattr(self, attr).as_dict()) for attr in field_names
        ])

        required_fields = [
            attr for attr in field_names if getattr(self, attr).required
        ]

        schema = {
            'type': 'object',
            'properties': properties,
            'required': required_fields
        }

        return schema
