from configparser import ConfigParser
from datetime import datetime
from typing import Any, List, Tuple, Union
from pathlib import Path

from utils.config import BASE_PATH, DATE_FORMAT, TIME_FORMAT


def parse_timestamp(
    atime: Any, strformat: str = f"{DATE_FORMAT} {TIME_FORMAT}"
) -> float:
    if not atime:
        raise TypeError("Cannot parse None to a timestamp!")

    if isinstance(atime, float):
        return atime
    try:
        return float(atime)
    except ValueError:
        # Cannot be converted
        pass

    ts = None
    # This will raise ValueError if it doesn't work
    date = datetime.strptime(atime, strformat)
    ts = date.timestamp()
    return ts


def parse_tags(tags: Any) -> float:
    if tags is None:
        raise TypeError("Cannot parse None to tags!")
    if isinstance(tags, tuple):
        return tags
    elif isinstance(tags, str):
        return tuple(tags.split(","))
    else:
        return tuple(str(tags))
