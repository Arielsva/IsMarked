from typing import Iterable
from datetime import date, datetime, timedelta, timezone

from appointment.models import Appointment
from appointment.libs import brasil_api


def get_available_times(date: date) -> Iterable[datetime]:

    if  brasil_api.is_holiday(date):
        return []

    start = datetime(year=date.year, month=date.month, day=date.day, hour=9, minute=0, tzinfo=timezone.utc)
    end = datetime(year=date.year, month=date.month, day=date.day, hour=18, minute=0, tzinfo=timezone.utc)
    delta = timedelta(minutes=30)

    available_times = set()

    while start < end:
        if not Appointment.objects.filter(date_time=start).exists():
            available_times.add(start)
        start += delta

    return available_times

def get_available_times_by_provider(provider, date: date) -> Iterable[datetime]:

    if  brasil_api.is_holiday(date):
        return []

    start = datetime(year=date.year, month=date.month, day=date.day, hour=9, minute=0, tzinfo=timezone.utc)
    end = datetime(year=date.year, month=date.month, day=date.day, hour=18, minute=0, tzinfo=timezone.utc)
    delta = timedelta(minutes=30)

    available_times = set()
    
    while start < end:
        if not Appointment.objects.filter(provider=provider,date_time=start).exists():
            available_times.add(start)
        start += delta

    return available_times