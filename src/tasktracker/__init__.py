import logging
from logging.handlers import RotatingFileHandler
from sys import stdout
from pathlib import Path


CONFIG = {
    "CSV": {
        "separator": ";",
    },
    "SHELVE": {
        "tasks_file": Path(__file__).parent.resolve() / Path("tasks_db"),
        "profiles_file": Path(__file__).parent.resolve() / Path("profiles_db"),
    },
    "DATES": {
        "timestamp_format": "%f", 
        "datetime_format": "%Y-%m-%dT%H:%M:%SZ",
        },
    "LOGGING": {
        "level": "DEBUG",
        "file": "tasktracker.log",
        "format": "%(asctime)s.%(msecs)03d %(levelname)s %(name)s %(funcName)s:%(lineno)d -> %(message)s",
        "time_format": "%Y-%m-%dT%H:%M:%S",
        "max_size": 1024**2 * 200,
        "backup_count": 5,
    },
}


def getCustomLogger(
    logger_name: str,
    custom_config: dict = {},
) -> logging.Logger:
    """Returns a logger with the name and configuration provided.

    Args:
        logger_name (str): A name for the logger instance.
        custom_config (dict, optional): A dictionary with the different configuration parametters. Defaults to {}.

    Raises:
        RuntimeError: custom_config param must be a dictionary-like object

    Returns:
        logging.Logger: A configured logger object.
    """

    if not isinstance(custom_config, dict):
        raise RuntimeError(
            "Cannot parse configuration provided! Type is %s" % type(custom_config)
        )

    level = custom_config.get("level", CONFIG["LOGGING"]["level"])
    file_path = custom_config.get("file", CONFIG["LOGGING"]["file"])
    format = custom_config.get("format", CONFIG["LOGGING"]["format"])
    time_format = custom_config.get("time_format", CONFIG["LOGGING"]["time_format"])
    max_size = custom_config.get("max_size", CONFIG["LOGGING"]["max_size"])
    backup_count = custom_config.get("backup_count", CONFIG["LOGGING"]["backup_count"])

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

    # logger.addHandler(handler_console)
    logger.addHandler(handler_file)

    return logger


logger = getCustomLogger("tasktracker.__init__")

if __name__ == "__main__":
    logger = getCustomLogger("test")
    logger.debug("debug message")
    logger.info("info message")
