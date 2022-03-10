from email.policy import default
from typing import Union

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from sys import stdout

from tasktracker.utils.config import load_config


def getCustomLogger(
    logger_name: str,
    config: dict = {},
) -> logging.Logger:
    """Returns a logger with the name and configuration provided.

    Args:
        logger_name (str): A name for the logger instance.
        config (dict, optional): A dictionary with the different configuration parametters. Defaults to {}.

    Raises:
        RuntimeError: config param must be a dictionary-like object

    Returns:
        logging.Logger: A configured logger object.
    """

    if not isinstance(config, dict):
        raise RuntimeError(
            "Cannot parse configuration provided! Type is %s" % type(config)
        )

    default_config = load_config("LOGGING")
    level = config.get("level", default_config["level"])
    file_path = config.get("file_path", default_config["file_path"])
    format = config.get("format", default_config["format"])
    time_format = config.get("time_format", default_config["time_format"])
    max_size = config.get("max_size", default_config["max_size"])
    backup_count = config.get("backup_count", default_config["backup_count"])

    logger = logging.getLogger(logger_name)
    logger.setLevel(level)

    formatter = logging.Formatter(
        format,
        time_format,
    )

    handler_console = logging.StreamHandler(stdout)
    handler_console.setFormatter(formatter)
    handler_console.setLevel(logging.INFO)

    handler_file = RotatingFileHandler(
        str(file_path),
        maxBytes=max_size,
        backupCount=backup_count,
    )
    handler_file.setFormatter(formatter)
    handler_file.setLevel(logging.DEBUG)

    logger.addHandler(handler_console)
    logger.addHandler(handler_file)

    return logger
