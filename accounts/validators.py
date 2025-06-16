from django.core.exceptions import ValidationError
import re

def validate_phone_number(value):
    pattern = r'^\+?1?\d{11,15}$'
    if not re.match(pattern, value):
        raise ValidationError("Неверный формат номера телефона.")