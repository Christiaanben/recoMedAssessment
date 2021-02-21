from datetime import datetime, timedelta

import holidays


def calculate_business_seconds(start_time: datetime, end_time: datetime) -> int:
    business_start_time = next_business_time(start_time)
    business_end_time = previous_business_time(end_time)
    if business_end_time <= business_start_time:
        return 0
    if business_start_time.date() == business_end_time.date():
        time_diff = business_end_time - business_start_time
        return int(time_diff.total_seconds())
    business_seconds_on_start_date = calculate_business_time_for_today_after(business_start_time)
    business_seconds_on_end_date = calculate_business_time_for_today_before(business_end_time)
    business_days_between_dates = calculate_business_days_between(business_start_time, business_end_time)
    return business_seconds_on_start_date + business_days_between_dates * 9 * 60 * 60 + business_seconds_on_end_date


def is_valid_iso8601(date_string) -> bool:
    try:
        parse_iso8601(date_string)
    except ValueError:
        return False
    return True


def parse_iso8601(date_string):
    return datetime.fromisoformat(date_string)


def is_holiday(date: datetime) -> bool:
    za_holidays = holidays.ZA()
    return date.date() in za_holidays


def is_weekend(date: datetime) -> bool:
    return date.weekday() in [5, 6]


def next_business_time(date: datetime) -> datetime:
    """
    Determines the first time from the given date that falls within business hours
    """
    if is_weekend(date) or is_holiday(date) or date.time() >= datetime(2000, 1, 1, 17).time():
        while is_weekend(date) or is_holiday(date) or date.time() >= datetime(2000, 1, 1, 17).time():
            date = (date + timedelta(days=1)).replace(hour=8)
        return date
    elif date.time() < datetime(2000, 1, 1, 8).time():
        return date.replace(hour=8)
    return date


def previous_business_time(date: datetime) -> datetime:
    """
    Determines the last time from the given date that falls within business hours
    """
    if date.time() > datetime(2000, 1, 1, 17).time():
        return date.replace(hour=17)
    if date.time() <= datetime(2000, 1, 1, 8).time():
        return (date - timedelta(days=1)).replace(hour=17)
    return date


def calculate_business_time_for_today_after(date: datetime) -> int:
    return int((date.replace(hour=17, minute=0, second=0) - date).total_seconds())


def calculate_business_time_for_today_before(date: datetime) -> int:
    return int((date - date.replace(hour=8, minute=0, second=0)).total_seconds())


def calculate_business_days_between(start_date: datetime, end_date: datetime) -> int:
    days = 0
    end_date -= timedelta(days=1)
    while start_date.date() < end_date.date():
        start_date += timedelta(days=1)
        if not (is_weekend(start_date) or is_holiday(start_date)):
            days += 1
    return days
