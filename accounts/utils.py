def adjust_phone_number(phone_number: str):
    if phone_number.startswith('8'):
        phone_number = '+7' + phone_number[1:]
    elif phone_number.startswith('7'):
        phone_number = '+' + phone_number
    return phone_number