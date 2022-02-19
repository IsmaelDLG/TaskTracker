from configparser import ConfigParser
from pathlib import Path

BASE_PATH = Path(__file__).parent.parent
DATE_FORMAT = "%d/%m/%Y"
TIME_FORMAT = "%H:%M"
CONFIG_FILE = BASE_PATH / Path("settings.ini")


if __name__ == "__main__":
    config = ConfigParser(allow_no_value=True)
    config["APP"] = {
        "# Global configuration for the application": None,
        "environment": "devel",
        "log_file": BASE_PATH / Path("tasktracker.log"),
        "log_format": "{datetime} {level} {user} {file}:{line} -> {message}",
    }

    config["DOMAIN"] = {
        "csv_default_delimiter": ";",
        "csv_default_headers": "start_time;end_time;pause;tags;notes",
    }

    config["PERSISTANCE"] = {
        "loglevel": "debug",
        "# Shelve config": None,
        "tasks_file": BASE_PATH / Path("tasksDB"),
        "profiles_file": BASE_PATH / Path("profilesDB"),
    }

    config["DEVEL"] = {"# Development configuration": None, "loglevel": "debug"}

    config["TEST"] = {
        "# Testing configuration": None,
        "loglevel": "debug",
    }

    config["PROD"] = {
        "# Production configuration": None,
        "loglevel": "info",
    }

    with open(str(CONFIG_FILE), "w") as f:
        config.write(f)


def load_config(config_file: str = None) -> ConfigParser:
    if not config_file:
        config_file = BASE_PATH / Path("settings.ini")
    conf = ConfigParser()
    with open(config_file, "r") as f:
        conf.read_file(f)
    return conf
