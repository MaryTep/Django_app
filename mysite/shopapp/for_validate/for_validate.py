import re

from django.core.exceptions import ValidationError
from django.template.defaultfilters import filesizeformat


def validate_positive(value):
#    price = self.cleaned_data.get('price')
    if value < 0:
        raise ValidationError(('Price must be a positive number.'),
                              params={'value': value},
                              )


def validate_0_100(value):
    if value < 0 or value > 100:
        raise ValidationError(('Discount must be between 0 and 100.'),
                              params={'value': value},
                              )


def validate_text(value):
    if not re.match(r'^[a-zA-Zа-яА-ЯёЁ0-9-_+.,;:?!@№$%&"()\'\s]+$', value):
        raise ValidationError(('Only letters, numbers, and special simbols are allowed (not allowed \' ).'),
                              params={'value': value},
                              )


def validate_email(value):
    if not re.match(r'^[a-zA-Z0-9-_@.\s]+$', value):
        raise ValidationError(('Only letters, numbers, spases, dot, and @ allowed.'),
                              params={'value': value},
                              )
