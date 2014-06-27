from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


class PhoneValidatorFR(RegexValidator):
    regex = r'^[0-9]{10}$'


class ZipCodeValidatorFR(RegexValidator):
    regex = r'^[0-9]{5}$'


# Validator model from scratch
def validate_even(value):
    if value % 2 != 0:
        raise ValidationError('%s is not an even number' % value)
