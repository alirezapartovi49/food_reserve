import re

from rest_framework.serializers import ValidationError
from django.utils.translation import gettext_lazy as _


_english_to_persian = {
    "0": "۰",
    "1": "۱",
    "2": "۲",
    "3": "۳",
    "4": "۴",
    "5": "۵",
    "6": "۶",
    "7": "۷",
    "8": "۸",
    "9": "۹",
}

_persian_to_english = {
    "۰": "0",
    "۱": "1",
    "۲": "2",
    "۳": "3",
    "۴": "4",
    "۵": "5",
    "۶": "6",
    "۷": "7",
    "۸": "8",
    "۹": "9",
}

persian_chars = [
" ",
    "آ",
    "ؤ",
    "ئ",
    "ا",
    "ب",
    "ة",
    "ت",
    "ث",
    "ج",
    "ح",
    "د",
    "خ",
    "ذ",
    "ر",
    "ز",
    "س",
    "ش",
    "ء",
    "ص",
    "ض",
    "ط",
    "ظ",
    "ع",
    "غ",
    "ف",
    "ق",
    "ل",
    "م",
    "ن",
    "ه",
    "و",
    "ی",
    "گ",
    "ک",
    "ژ",
    "چ",
    "پ",
"٫",
]


def persian_to_english(number: str) -> str:
    number = str(number)
    num = str()

    for i in number:
        item = _persian_to_english.get(i)
        if item:
            num += item
        else:
            item = _english_to_persian.get(i)
            if item:
                num += i
    return num


def is_persian(field: str) -> object or None:
    """used for check full name is persian"""

    for i in field:
        if i not in persian_chars:
            if i not in _english_to_persian:
                if i not in _persian_to_english:
                    raise ValidationError("the field must be persian or not have invalid chars")
    return field
