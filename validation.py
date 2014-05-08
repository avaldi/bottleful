

class BaseField(object):
    """ Base class used by BaseSchema to define the fields of the schema.
    """

    def __init__(self, field_type, field_format=None, required=False,
                 primary_key=False):

        self.field_type = field_type
        self.field_format = field_format
        self.required = required
        self.primary_key = primary_key

    def as_dict(self):
        """ Returns a dict representing the field in a format that can be
        used by jsonschema validation library.
        """

        result = {
            'type': self.field_type,
        }

        if self.field_format:
            result.update({
                'format': self.field_format,
            })

        return result


class BaseSchema(object):
    """ Base class used to define the structure of the data coming
    from the clients.
    """

    @classmethod
    def field_names(cls):
        """ Generator that yields the names of the fields defined in this
        schema class.
        """

        for attr in dir(cls):
            if isinstance(getattr(cls, attr), BaseField):
                yield attr

    @classmethod
    def primary_key(cls):
        """ Returns the primary key of this schema class.
        """

        primary_keys = [
            attr for attr in cls.field_names() if getattr(cls, attr).primary_key
        ]

        if not primary_keys:
            return None

        if len(primary_keys) == 1:
            return primary_keys[0]

        return primary_keys

    @classmethod
    def _generate_json_schema(cls):
        """ Generate the dictionary containing the validation rules to be
        used with the json-schema validator.
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

    @classmethod
    def as_json_schema(cls):
        """ Returns the generated json-schema dictionary.
        """

        if not hasattr(cls, '_schema'):
            cls._schema = cls._generate_json_schema()

        return cls._schema
