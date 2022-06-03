from cmath import log
import csv
from pathlib import Path
from time import time
from typing import List, Tuple

from tasktracker import getCustomLogger, CONFIG
from tasktracker.domain.DomainCtlInt import DomainCtlInt
from tasktracker.persistance.ShelvePersistance import ShelvePersistance


class DomainCtlImp(DomainCtlInt):
    def __init__(self) -> None:
        super().__init__()
        self.config = {"csv": CONFIG["CSV"]}
        self.persistanceCtl = ShelvePersistance()

    def create_task(
        self,
        creation_time: float,
        start_time: float,
        end_time: float,
        pause_time: float,
        tags: Tuple[str],
        notes: str,
    ) -> object:
        if creation_time is None or start_time is None:
            # Its ok if end_time is None!
            logger.error(f"creation_time: {creation_time} start_time: {start_time}")
            raise RuntimeError("creation_time and start_time must be defined!")
        if not (type(tags) in (list, tuple, str)):
            logger.error(f"tags has wrong type: {type(tags)} tags: {tags}")
            raise RuntimeError("creation_time and start_time must be defined!")

        return self.persistanceCtl.create_task(
            creation_time, start_time, end_time, pause_time, tags, notes
        )

    def get_task(self, id: int) -> object:
        return self.persistanceCtl.get_task(id)

    def get_last_task(self) -> object:
        return self.persistanceCtl.get_task(self.persistanceCtl.get_task_last_id())

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
                    logger.debug("Got task: {}".format(task))
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
                logger.debug(row)
                self.create_task(
                    row.get("creation_time", time()),
                    row.get("start_time", None),
                    row.get("end_time", None),
                    row.get("pause", 0),
                    row.get("tags", ""),
                    row.get("notes", ""),
                )


logger = getCustomLogger("domain.DomainCtlImp")
