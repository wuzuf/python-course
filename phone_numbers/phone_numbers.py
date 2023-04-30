def format_phone_number(func):

    def inner(phone):
        new_phone = func(phone)
        if len(new_phone) == 12:
            return f'+{new_phone}'
        if len(new_phone) < 12:
            return f'+38{new_phone}'

    return inner


@format_phone_number
def sanitize_phone_number(phone):
    new_phone = (phone.strip().removeprefix("+").replace("(", "").replace(
        ")", "").replace("-", "").replace(" ", ""))
    return new_phone


print(sanitize_phone_number("0777-34-64-26"))