from datetime import datetime
import birthdays

input = {
    'Nick': datetime(year=1962, month=4, day=28),
    'Jane': datetime(year=2004, month=4, day=29),
    'Anton': datetime(year=1987, month=4, day=25),
    'John': datetime(year=2020, month=9, day=23),
    'Kate': datetime(year=1995, month=3, day=23),
    'Oleg': datetime(year=1989, month=4, day=24),
    'Helen': datetime(year=2004, month=4, day=22),
    'Mike': datetime(year=2001, month=1, day=1),
    'Olga': datetime(year=1995, month=4, day=23),
    'Gab': datetime(year=2001, month=1, day=5),
}


def test_birthdays():
    greetings = birthdays.reminder(input, datetime(2023, 4, 22, 22, 12, 0))
    assert greetings == """Monday: Oleg, Helen, Olga
Tuesday: Anton
Friday: Nick"""

    greetings = birthdays.reminder(input, datetime(2023, 4, 23))
    assert greetings == """Monday: Oleg, Helen, Olga
Tuesday: Anton
Friday: Nick"""


def test_birthdays_next_week():
    greetings = birthdays.reminder(input, datetime(2023, 4, 17))
    assert greetings == """Monday: Oleg, Helen, Olga
Tuesday: Anton
Friday: Nick"""


def test_birthdays_none():
    greetings = birthdays.reminder(input, datetime(2023, 5, 17))
    assert greetings == ""


def test_birthdays_change_of_year():
    greetings = birthdays.reminder(input, datetime(2023, 12, 26))
    assert greetings == "Monday: Mike\nFriday: Gab"