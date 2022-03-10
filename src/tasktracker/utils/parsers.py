from configparser import ConfigParser
from datetime import datetime
from multiprocessing.sharedctypes import Value
from typing import Any, List, Tuple, Union
from pathlib import Path

from tasktracker.utils.logging import getCustomLogger


logger = getCustomLogger(__name__)


def parse_timestamp(atime: Any, strformats: Union[List[str], Tuple[str]]) -> float:
    if not atime:
        raise TypeError("Cannot parse None to a timestamp!")

    if isinstance(atime, float):
        return atime
    try:
        return float(atime)
    except ValueError:
        # Cannot be converted
        logger.debug(f"Could not convert time string to float!")

    if type(strformats) in (list, tuple):
        for f in strformats:
            try:
                # This will raise ValueError if it doesn't work
                date = datetime.strptime(atime, f)
                ts = date.timestamp()
                return ts
            except:
                logger.debug(f"Could not parse string using format: {f}")

    # Raise exception to be consistent
    exc = ValueError(f"Time {atime} could not be parsed!")
    logger.exception(exc)
    raise exc


def parse_tags(tags: Any) -> float:
    if tags is None:
        raise TypeError("Cannot parse None to tags!")
    if isinstance(tags, tuple):
        return tags
    elif isinstance(tags, str):
        return tuple(tags.split(","))
    else:
        return tuple(str(tags))
