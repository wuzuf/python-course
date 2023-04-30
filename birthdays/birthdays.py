import collections
from datetime import datetime, timedelta, date, time


def reminder(input, today=datetime.today()):
    # Force the time to 00:00:00
    today = datetime.combine(today, time.min)
    # Create a dictionary k=day to greet, v=people to greet
    bdays = collections.defaultdict(list)
    # Next monday is today + 7 days - current weekday
    next_monday = today + timedelta(days=7 - today.weekday())
    # Next saturday (can be in the past if you are already on sunday) is next monday -2 days
    next_saturday = next_monday + timedelta(days=-2)
    # Iterate on people
    for name, birth in input.items():
        # birthday is the birth day/month for the current year
        birthday = birth.replace(year=today.year)
        # If the birthday is before the saturday, we need to check if next birthday (so year+1) is coming close
        if birthday < next_saturday:
            birthday = birth.replace(year=today.year + 1)
        # If we are more than 7 days before the birthday, we can move on
        if birthday - next_saturday >= timedelta(days=7):
            continue

        # Otherwise, we need to greet
        # If the day is Sat/Sun, greet on Monday
        if birthday.weekday() > 4:
            bdays[next_monday].append(name)
        else:
            bdays[birthday].append(name)

    # Build output
    res = []
    # Sort on keys (which are the days to greet people) to be sure to have the right order
    for birthday in sorted(bdays.keys()):
        # %A gives the day in full local name (https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes)
        day = birthday.strftime("%A")
        res.append(day + ": " + ", ".join(bdays[birthday]))
    return "\n".join(res)
