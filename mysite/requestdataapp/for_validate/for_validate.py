import re

from django.core.exceptions import ValidationError
from django.template.defaultfilters import filesizeformat


def validate_positive(value):
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


def validate_file_size(value, max_size=5242880):
    if value > max_size:
        v_max_size = re.search(r'\d*', filesizeformat(max_size)).group() + " MB"
        v_value_size = re.search(r'\d*', filesizeformat(value)).group() + " MB"
        return f'Файл не сохранен. Размер файла должен быть менее {v_max_size}. Размер выбранного файла: {v_value_size}.'
        # raise ValidationError(f'Файл не сохранен. Размер файла должен быть менее {v_max_size}. '
        #                       f'Размер выбранного файла: {v_value_size}.',
        #                       params={'v_max_size': v_max_size, 'v_value_size': v_value_size}
        #                       )


def validate_ip(value):
    if not re.match(r'^[0-9.]+$', value):
        raise ValidationError(('Only numbers and dot allowed.'),
                              params={'value': value},
                              )

