# pylint: disable=R0904

import unittest

import nose

from boapi.validation import BaseField
from boapi.validation import BaseSchema


class TestBaseField(unittest.TestCase):
    """ Test BaseField functionality
    """

    def test_dict_transformation_with_format(self):
        """ Test .as_dict() transformation when a field format has been set
        """

        field = BaseField(
            field_type='string',
            field_format='email'
        )

        expected_result = {
            'type': 'string',
            'format': 'email'
        }

        result = field.as_dict()

        nose.tools.assert_equals(result, expected_result)

    def test_dict_transformation_without_format(self):
        """ Test .as_dict() transformation when no field format has been set
        """

        field = BaseField(
            field_type='string',
        )

        expected_result = {
            'type': 'string',
        }

        result = field.as_dict()

        nose.tools.assert_equals(result, expected_result)


class TestBaseSchema(unittest.TestCase):
    """ Test BaseSchema functionality
    """

    class FakeSchemaWithoutPK(BaseSchema):
        """ Fake schema without a PK field
        """
        email = BaseField('string')
        mobile = BaseField('string')
        fake_field = BaseField('string')

    class FakeSchemaSinglePK(FakeSchemaWithoutPK):
        """ Fake schema with a single PK field
        """
        uuid = BaseField('string', primary_key=True)

    class FakeSchemaMultiplePK(FakeSchemaSinglePK):
        """ Fake schema with multiple PK fields
        """
        uuid2 = BaseField('string', primary_key=True)

    def test_field_names_generation(self):
        """ Test that the field names returned by .field_names() are correct
        """

        expected_field_names = set(['uuid', 'email', 'mobile', 'fake_field'])

        field_names = set([f for f in self.FakeSchemaSinglePK.field_names()])

        nose.tools.assert_equals(field_names, expected_field_names)

    def test_no_primary_key(self):
        """ Test the primary_key value when no field is set as PK
        """
        expected_pk = None

        pk_name = self.FakeSchemaWithoutPK.primary_key()

        nose.tools.assert_equals(pk_name, expected_pk)

    def test_single_primary_key(self):
        """ Test the primary_key value when one field is set as PK
        """
        expected_pk = 'uuid'

        pk_name = self.FakeSchemaSinglePK.primary_key()

        nose.tools.assert_equals(pk_name, expected_pk)

    def test_multiple_primary_key(self):
        """ Test the primary_key value when multiple fields are set as PK
        """
        expected_pks = set(['uuid', 'uuid2'])

        pk_set = set(self.FakeSchemaMultiplePK.primary_key())

        nose.tools.assert_equals(pk_set, expected_pks)

