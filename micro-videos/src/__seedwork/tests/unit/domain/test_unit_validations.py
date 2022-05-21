from datetime import datetime
import unittest
from dataclasses import fields
from __seedwork.domain.validators import (
    ValidatorFieldsInterface,
    ValidatorRules
)
from __seedwork.domain.exceptions import SimpleValidationException


class TestValidationRulesUnit(unittest.TestCase):

    def test_algumacoisa(self):
        validator = ValidatorRules.values('test', 'field')
        self.assertIsInstance(validator, ValidatorRules)
        self.assertEqual('test', validator.value)
        self.assertEqual('field', validator.prop)

    def test_required_rule(self):
        data = [
            {'value': "test", 'prop': "field"},
            {'value': 5, 'prop': "field"},
            {'value': 0, 'prop': "field"},
            {'value': False, 'prop': "field"},
        ]

        for i in data:
            self.assertIsInstance(
                ValidatorRules.values(i['value'], i['prop']).required(),
                ValidatorRules
            )

        data = [
            {'value': None, 'prop': "field"},
            {'value': "", 'prop': "field"},
        ]

        message_error = 'The field is required'

        for i in data:
            with self.assertRaises(SimpleValidationException) as assert_error:
                ValidatorRules.values(i['value'], i['prop']).required()
            self.assertEqual(message_error, assert_error.exception.args[0])

    def test_string_rule(self):
        data = [
            {'value': None, 'prop': "field"},
            {'value': "", 'prop': "field"},
            {'value': "test", 'prop': "field"},
        ]

        for i in data:
            self.assertIsInstance(
                ValidatorRules.values(i['value'], i['prop']).string(),
                ValidatorRules
            )

        data = [
            {'value': 5, 'prop': "field"},
            {'value': datetime, 'prop': "field"},
        ]

        message_error = 'The field must be a string'

        for i in data:
            with self.assertRaises(SimpleValidationException) as assert_error:
                ValidatorRules.values(i['value'], i['prop']).string()
            self.assertEqual(message_error, assert_error.exception.args[0])

    def test_max_length_rule(self):
        data = [
            {'value': None, 'prop': "field"},
            {'value': "t" * 5, 'prop': "field"},
        ]

        for i in data:
            self.assertIsInstance(
                ValidatorRules.values(i['value'], i['prop']).max_length(5),
                ValidatorRules
            )

        data = [
            {'value': "t" * 11, 'prop': "field"},
        ]

        message_error = 'The field must be less than 10 characters'

        for i in data:
            with self.assertRaises(SimpleValidationException) as assert_error:
                ValidatorRules.values(i['value'], i['prop']).max_length(10)
            self.assertEqual(message_error, assert_error.exception.args[0])

    def test_boolean_rule(self):
        data = [
            {'value': None, 'prop': "field"},
            {'value': True, 'prop': "field"},
            {'value': False, 'prop': "field"},
        ]

        for i in data:
            self.assertIsInstance(
                ValidatorRules.values(i['value'], i['prop']).boolean(),
                ValidatorRules
            )

        data = [
            {'value': "", 'prop': "field"},
            {'value': 5, 'prop': "field"},
        ]

        message_error = 'The field must be a boolean'

        for i in data:
            with self.assertRaises(SimpleValidationException) as assert_error:
                ValidatorRules.values(i['value'], i['prop']).boolean()
            self.assertEqual(message_error, assert_error.exception.args[0])


class TestValidatorFieldsInterfaceUnit(unittest.TestCase):

    def test_throw_error_when_methods_not_implemented(self):
        with self.assertRaises(TypeError) as assert_error:
            # pylint: disable=abstract-class-instantiated
            ValidatorFieldsInterface()
        self.assertEqual(
            "Can't instantiate abstract class ValidatorFieldsInterface " +
            "with abstract method validate",
            assert_error.exception.args[0]
        )

    def test_errors_attribute_is_none(self):
        fields_class = fields(ValidatorFieldsInterface)
        self.assertEqual(fields_class[0].name, 'errors')
        self.assertIsNone(fields_class[0].default)
