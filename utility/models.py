from django.db import models

import dataclasses
from typing import List, Tuple, Dict


class ChoicesMeta(type):
    REAL_ACCESS_TO_CHOICE_FLAG = "__real"

    def __getattribute__(cls, item: str):
        if item in ["Choice", "REAL_ACCESS_TO_CHOICE_FLAG"]:
            return super().__getattribute__(item)

        attr = super().__getattribute__(item)
        if isinstance(attr, Choices.Choice):
            return attr.value
        return attr


class Choices(metaclass=ChoicesMeta):
    @dataclasses.dataclass
    class Choice:
        value: str
        verbose: str

    @classmethod
    def _get_choices(cls) -> List[Choice]:
        choices = []
        vars_ = vars(cls)
        for attr in vars_:
            attribute = vars_[attr]
            if isinstance(attribute, cls.Choice):
                choices.append(attribute)
        return choices

    @classmethod
    def get_choices(cls) -> Tuple[Tuple[str, str], ...]:
        choices = []
        for choice in cls._get_choices():
            choices.append((choice.value, choice.verbose))
        return tuple(choices)

    @classmethod
    def get_translator(cls) -> Dict[str, str]:
        return dict(cls.get_choices())

