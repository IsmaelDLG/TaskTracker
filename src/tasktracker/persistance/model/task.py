from ctypes import util
from typing import Dict, List, Tuple
from datetime import datetime
from tasktracker import CONFIG


class Task:
    def __init__(
        self,
        id: int,
        creation_time: float,
        start_time: float,
        end_time: float,
        pause: float,
        tags: List[str],
        notes: str,
    ) -> None:

        if not end_time is None and end_time - start_time - pause < 0:
            raise ValueError("Dedication < 0!")

        self.id = id
        self.creation_time = creation_time
        self.start_time = start_time
        self.end_time = end_time
        self.pause = pause
        self.tags = tags
        self.notes = notes

    def dedication(self) -> float:
        """Returns dedication (in hours) of this task

        Returns:
            float: Hours spent in from start_time to end_time, not taking into account the pause time
        """

        return (
            (self.end_time - self.start_time - self.pause) / (60 * 60)
            if not self.end_time is None
            else 0
        )

    def keys(self) -> Tuple[str]:
        return (
            "id",
            "creation_time",
            "start_time",
            "end_time",
            "pause",
            "dedication",
            "tags",
        )

    def values(self) -> tuple:
        return (
            self.id,
            self.creation_time,
            self.start_time,
            self.end_time,
            self.pause,
            self.dedication(),
            self.tags,
        )

    def values_str(self, human_readable=False) -> Tuple[str]:
        vals = None
        dedic = self.dedication()
        if human_readable:
            vals = (
                str(self.id),
                datetime.fromtimestamp(self.creation_time).strftime(
                    CONFIG["DATES"]["datetime_format"]
                ),
                datetime.fromtimestamp(self.start_time).strftime(
                    CONFIG["DATES"]["datetime_format"]
                ),
                datetime.fromtimestamp(self.end_time).strftime(
                    CONFIG["DATES"]["datetime_format"]
                )
                if not self.end_time is None
                else "",
                str(round(self.pause, 2)),
                str(round(dedic, 2)) if dedic != 0 else "",
                ",".join(self.tags),
            )
        else:
            vals = (
                str(self.id),
                str(self.creation_time),
                str(self.start_time),
                str(self.end_time),
                str(self.pause),
                str(self.dedication()),
                ",".join(self.tags),
            )
        return vals

    def __str__(self) -> str:
        return 'Task<id: {} start_time: "{}", end_time: "{}", pause: {}, tags: "{}", notes: "{}">'.format(
            self.id,
            datetime.fromtimestamp(self.start_time).strftime(
                CONFIG["DATES"]["datetime_format"]
            ),
            datetime.fromtimestamp(self.end_time).strftime(
                CONFIG["DATES"]["datetime_format"]
            )
            if not self.end_time is None
            else "",
            self.pause,
            ", ".join(self.tags),
            self.notes[:25],
        )

    def __repr__(self) -> str:
        return '{{"id": {}, "creation_time": {}, "start_time": {}, "end_time": {}, "pause": {}, "tags": "{}", "notes": "{}"}}'.format(
            self.id,
            self.creation_time,
            self.start_time,
            self.end_time,
            self.pause,
            ", ".join(self.tags),
            self.notes,
        )


if __name__ == "__main__":
    a = Task(1, 2, 0, 3600, 0, ["test", "tag"], "A note")
    print(str(a))
    print(repr(a))
    print(a.dedication())
