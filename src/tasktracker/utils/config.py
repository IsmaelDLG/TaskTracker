from pathlib import Path

BASE_PATH = Path(".").parent


def load_config(key: str = None) -> dict:
    if isinstance(key, str):

        def raise_(ex):
            raise ex

        return CONFIGURATIONS.get(
            key, lambda: raise_(RuntimeError("Requested configuration doesn't exist!"))
        )()
    else:
        return {k: v() for k, v in CONFIGURATIONS.items()}


def logging_config() -> dict:
    return {
        "level": "DEBUG",
        "file": BASE_PATH / Path("tasktracker.log"),
        "format": "%(asctime)s %(levelname)s %(module)s:%(lineno)s -> %(message)s",
        "time_format": "%Y-%m-%dT%H:%M:%S%z",
        "max_size": 500 * 1024**2,
        "backup_count": 5,
    }


def csv_config():
    return {
        "delimiter": ";",
        "import_headers": "start_time;end_time;pause;tags;notes",
        "export_headers": "start_time;end_time;pause;dedication;tags;notes",
    }


def shelve_config():
    return {
        "tasks_path": BASE_PATH / Path("TasksDB"),
        "profiles_path": BASE_PATH / Path("ProfilesDB"),
        "time_format": "%Y-%m-%d %H:%M:%S",
    }


def cli_config():
    return {
        "input_time_formats": [
            "%Y-%m-%dT%H:%M:%S%z",
            "%Y-%m-%d %H:%M:%S",
            "%H:%M:%S",
            "%s",
        ]
    }


CONFIGURATIONS = {
    "LOGGING": logging_config,
    "CSV": csv_config,
    "PERSISTANCE": shelve_config,
    "CLI": cli_config,
}
if __name__ == "__main__":
    print(load_config("LOGGING"))
    print(load_config())
