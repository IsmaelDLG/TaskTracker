import csv
from pathlib import Path
from time import time
from typing import List, Tuple

from tasktracker.domain.DomainCtlInt import DomainCtlInt
from tasktracker.persistance.model.task import Task
from tasktracker.persistance.ShelvePersistance import (
    ShelvePersistance as persistanceCtl,
)
from tasktracker.utils.parsers import parse_timestamp, parse_tags


class DomainCtlImpl(DomainCtlInt):
    def __init__(self, config) -> None:
        super().__init__()
        self.config = config["DOMAIN"]
        self.persistanceCtl = persistanceCtl(config["PERSISTANCE"])

    def create_task(
        self,
        creation_time: float,
        start_time: float,
        end_time: float,
        pause_time: float,
        tags: Tuple[str],
        notes: str,
    ) -> Task:
        # Validation
        creation_time = parse_timestamp(creation_time)
        start_time = parse_timestamp(start_time)
        if end_time:
            end_time = parse_timestamp(end_time)
        # Its ok if end_time is None!
        pause_time = float(pause_time)
        tags = parse_tags(tags)
        notes = str(notes)
        # Proceed
        return self.persistanceCtl.create_task(
            creation_time, start_time, end_time, pause_time, tags, notes
        )

    def get_task(self, id: int):
        self.persistanceCtl.get_task(id)

    def export_as_csv(
        self, file: Path, headers: bool = False, human_readable: bool = False
    ):
        with open(file, "w", newline="") as fd:
            csvwriter = csv.writer(
                fd, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL
            )
            max = self.persistanceCtl.get_task_last_id()
            for i in range(1, max + 1):
                task = None
                try:
                    task = self.persistanceCtl.get_task(i)
                    print("Got task: {}".format(task))
                except KeyError:
                    continue
                if headers:
                    csvwriter.writerow(task.keys())
                str_values = task.values_str(human_readable)
                csvwriter.writerow(str_values)
                headers = False

    def import_from_csv(self, file: Path, headers: bool = False) -> None:
        with open(str(file), newline="") as csvfile:
            rows = ()
            if headers:
                rows = csv.DictReader(csvfile, delimiter=";")
            else:
                rows = csv.DictReader(
                    csvfile,
                    delimiter=";",
                    fieldnames=self.config["csv_default_headers"].split(
                        self.config["csv_default_delimiter"]
                    ),
                )
            for row in rows:
                print(row)
                self.create_task(
                    row.get("creation_time", time()),
                    row.get("start_time", None),
                    row.get("end_time", None),
                    row.get("pause", 0),
                    row.get("tags", ""),
                    row.get("notes", ""),
                )
