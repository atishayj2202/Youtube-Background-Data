from datetime import datetime

import pytz


def get_current_time():
    return datetime.now(tz=pytz.utc)


def parse_time_str_to_tz(time_str: str) -> datetime:
    return datetime.fromisoformat(time_str.replace("Z", "+00:00")).astimezone(
        tz=pytz.utc
    )


def parse_time_tz_to_str(time: datetime) -> str:
    return time.astimezone(tz=pytz.timezone("Asia/Kolkata")).strftime(
        "%I:%M:%S %p %d %B %Y"
    )


def parse_time_datetime_to_tz(time: datetime) -> datetime:
    return time.astimezone(tz=pytz.utc)
