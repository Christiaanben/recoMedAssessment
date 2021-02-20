from datetime import datetime, timedelta

import holidays


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


def next_business_time(date: datetime) -> datetime:
    """
    Determines the first time from the given date that falls within business hours
    """
    if date.time() < datetime(2000, 1, 1, 8).time():
        return date.replace(hour=8)
    if date.time() >= datetime(2000, 1, 1, 17).time():
        return (date + timedelta(days=1)).replace(hour=8)
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
        if start_date.weekday() < 5:
            days += 1
    return days
