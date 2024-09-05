import datetime
from collections import Counter


def get_week_counts():
    remaining_days = []
    current_day = datetime.date.today()
    current_month, current_year = current_day.month, current_day.year
    if current_month == 12:
        last_day_of_month = datetime.date(current_year, 12, 31)
    else:
        first_day_of_next_month = datetime.date(current_year, current_month + 1, 1)
        last_day_of_month = first_day_of_next_month - datetime.timedelta(days=1)
    while current_day <= last_day_of_month:
        remaining_days.append(current_day.weekday())
        current_day += datetime.timedelta(days=1)
    result = {day: count for day, count in Counter(remaining_days).items()}
    return result
