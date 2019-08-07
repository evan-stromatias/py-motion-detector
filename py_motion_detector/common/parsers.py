import datetime
from typing import Optional


def str2time_duration(duration: Optional[str]) -> Optional[datetime.datetime.time]:
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
        raise ValueError("Please use one of the following time units: h for hours, m for minutes or s for seconds instead of {}".format(duration_units))
    duration = datetime.datetime.strptime(duration_num, strp).time()
    return duration


def str2time_start_processing_time(from_time: Optional[str]) -> datetime.datetime.time:
    if from_time is None:
        return None
    from_time = datetime.datetime.strptime(from_time, '%H:%M:%S').time()
    return from_time
