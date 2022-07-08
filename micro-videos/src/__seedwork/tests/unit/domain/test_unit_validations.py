from datetime import datetime
import unittest
from dataclasses import fields
from __seedwork.domain.validators import (
    ValidatorFieldsInterface,
    ValidatorRules
)
from __seedwork.domain.exceptions import SimpleValidationException


class TestValidationRulesUnit(unittest.TestCase):

    def test_values_method(self):
        validator = ValidatorRules.values('some value', 'prop')
        self.assertIsInstance(validator, ValidatorRules)
        self.assertEqual('some value', validator.value)
        self.assertEqual('prop', validator.prop)

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

        invalid_data = [
            {'value': None, 'prop': "field"},
            {'value': "", 'prop': "field"},
        ]

        message_error = 'The field is required'

        for i in invalid_data:
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

        invalid_data = [
            {'value': 5, 'prop': "field"},
            {'value': datetime, 'prop': "field"},
            {'value': {}, 'prop': "field"},
            {'value': True, 'prop': "field"},
        ]

        message_error = 'The field must be a string'

        for i in invalid_data:
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

        invalid_data = [
            {'value': "t" * 11, 'prop': "field"},
        ]

        message_error = 'The field must be less than 10 characters'

        for i in invalid_data:
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

        invalid_data = [
            {'value': "", 'prop': "field"},
            {'value': 5, 'prop': "field"},
            {'value': {}, 'prop': "field"}
        ]

        message_error = 'The field must be a boolean'

        for i in invalid_data:
            with self.assertRaises(SimpleValidationException) as assert_error:
                ValidatorRules.values(i['value'], i['prop']).boolean()
            self.assertEqual(message_error, assert_error.exception.args[0])

    def test_throw_a_validation_exception_when_combine_two_or_more_rules(self):
        with self.assertRaises(SimpleValidationException) as assert_error:
            # pylint: disable=expression-not-assigned
            ValidatorRules.values(
                None,
                'prop'
            ).required().string().max_length(5)
            self.assertEqual(
                'The prop is required',
                assert_error.exception.args[0],
            )

        with self.assertRaises(SimpleValidationException) as assert_error:
            # pylint: disable=expression-not-assigned
            ValidatorRules.values(
                5,
                'prop'
            ).required().string().max_length(5)
            self.assertEqual(
                'The prop must be a string',
                assert_error.exception.args[0],
            )

        with self.assertRaises(SimpleValidationException) as assert_error:
            # pylint: disable=expression-not-assigned
            ValidatorRules.values(
                "t" * 6,
                'prop'
            ).required().string().max_length(5)
            self.assertEqual(
                'The prop must be less than 5 characters',
                assert_error.exception.args[0],
            )

        with self.assertRaises(SimpleValidationException) as assert_error:
            # pylint: disable=expression-not-assigned
            ValidatorRules.values(
                None,
                'prop'
            ).required().boolean()
            self.assertEqual(
                'The prop is required',
                assert_error.exception.args[0],
            )

        with self.assertRaises(SimpleValidationException) as assert_error:
            # pylint: disable=expression-not-assigned
            ValidatorRules.values(
                5,
                'prop'
            ).required().boolean()
            self.assertEqual(
                'The prop must be a boolean',
                assert_error.exception.args[0],
            )

    def test_valid_cases_for_combination_between_rules(self):
        ValidatorRules('test', 'prop').required().string()
        ValidatorRules("t" * 5, 'prop').required().string().max_length(5)

        ValidatorRules(True, 'prop').required().boolean()
        ValidatorRules(False, 'prop').required().boolean()
        # pylint: disable=redundant-unittest-assert
        self.assertTrue(True)


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
