
from abc import ABC
import abc
from dataclasses import dataclass
from typing import Any, Dict, List
from __seedwork.domain.exceptions import (
    SimpleValidationException,
    NotImplementedException
)


@dataclass(frozen=True, slots=True)
class ValidatorRules:
    value: Any
    prop: str

    @staticmethod
    def values(value, prop):
        return ValidatorRules(value, prop)

    def required(self) -> 'ValidatorRules':
        if self.value is None or self.value == '':
            raise SimpleValidationException(f'The {self.prop} is required')
        return self

    def string(self) -> 'ValidatorRules':
        if self.value is not None and not isinstance(self.value, str):
            raise SimpleValidationException(
                f'The {self.prop} must be a string')
        return self

    def max_length(self, max_length: int) -> 'ValidatorRules':
        if self.value is not None and len(self.value) > max_length:
            raise SimpleValidationException(
                f'The {self.prop} must be less than {max_length} characters'
            )
        return self

    def boolean(self) -> 'ValidatorRules':
        if self.value is not None and self.value is not True and self.value is not False:
            raise SimpleValidationException(
                f'The {self.prop} must be a boolean'
            )
        return self


ErrorFields = Dict[str, List[str]]


@dataclass(slots=True,)
class ValidatorFieldsInterface(ABC):
    errors: ErrorFields = None

    @abc.abstractmethod
    def validate(self, data: Any) -> None:
        raise NotImplementedException
