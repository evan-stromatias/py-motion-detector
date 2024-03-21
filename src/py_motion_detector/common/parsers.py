import datetime
from typing import Optional


def str2time_duration(duration: str | None) -> Optional[datetime.datetime.time]:
    """
    Converts a string to a `datetime.datetime.time` object.

    Args:
        duration: A string representing time duration in the format: #h/m/s where # is a number and
            h=hours, m=minutes, s=seconds.

    Returns:
        A `datetime.datetime.time` object if `duration` is not `None`, otherwise `None`

    Raises:
        ValueError: If the `duration` format is incorrect.
    """
    if duration is None:
        return None

    duration_num = duration[:-1]
    duration_units = duration[-1]
    if duration_units.lower() == 'h':
        strp = "%H"
    elif duration_units.lower() == 'm':
        strp = "%M"
    elif duration_units.lower() == 's':
        strp = "%S"
    else:
        raise ValueError(
            "Please use one of the following time units: h for hours, m for minutes or s for seconds "
            f"instead of {duration_units}"
        )
    duration = datetime.datetime.strptime(duration_num, strp).time()
    return duration


def str2time_start_processing_time(from_time: str | None) -> Optional[datetime.datetime.time]:
    """
    Converts a string to a `datetime.datetime.time` object.

    Args:
        from_time: A string representing time.

    Returns:
        A `datetime.datetime.time` object if `from_time` is not `None`, otherwise returns `None`

    """
    if from_time is None:
        return None

    from_time = datetime.datetime.strptime(from_time, '%H:%M:%S').time()
    return from_time
