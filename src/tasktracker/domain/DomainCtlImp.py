from cmath import log
import csv
from datetime import datetime
from pathlib import Path
from time import time
from typing import List, Tuple

from tasktracker import getCustomLogger, CONFIG
from tasktracker.domain.DomainCtlInt import DomainCtlInt
from tasktracker.persistance.ShelvePersistance import ShelvePersistance
from tasktracker.persistance.model.task import Task

logger = getCustomLogger("domain.DomainCtlImp")


class DomainCtlImp(DomainCtlInt):
    def __init__(self) -> None:
        super().__init__()
        self.config = {"csv": CONFIG["CSV"]}
        self.persistanceCtl = ShelvePersistance()

    def create_task(
        self,
        start_time: float,
        end_time: float,
        pause_time: float,
        tags: Tuple[str],
        notes: str,
    ) -> object:
        creation_time = datetime.utcnow()
        if start_time is None:
            # Its ok if end_time is None!
            logger.error(f"creation_time: {creation_time} start_time: {start_time}")
            raise RuntimeError("creation_time and start_time must be defined!")
        if not (type(tags) in (list, tuple, str)):
            logger.error(f"tags has wrong type: {type(tags)} tags: {tags}")
            raise RuntimeError("creation_time and start_time must be defined!")

        newtask = Task(
            None, creation_time, start_time, end_time, pause_time, tags, notes
        )
        logger.debug(f":create_task task: {newtask}")
        return self.persistanceCtl.save_task(newtask)

    def get_task(self, id: int) -> object:
        """_summary_

        Args:
            id (int): ID of the task to return

        Raises:
            e: _description_

        Returns:
            object: _description_
        """
        try:
            return self.persistanceCtl.get_task(id)
        except IndexError as e:
            logger.error(f"Could not get task with id: {id}! error: {e}")
            raise e

    def get_last_task(self) -> object:
        """_summary_

        Raises:
            e: _description_

        Returns:
            object: _description_
        """
        try:
            return self.persistanceCtl.get_task(self.persistanceCtl.get_task_last_id())
        except IndexError as e:
            logger.error(f"Could not get last task! error: {e}")
            raise e

    def edit_task(self, start_time, end_time, pause, tags, notes) -> object:
        """Edit a task, if it exists

        Returns:
            object: _description_
        """
        task = self.get_task(id)
        if start_time:
            task.start_time = start_time
        if end_time:
            task.end_time = end_time
        if pause:
            task.pause = pause
        if tags:
            task.tags = tags
        if notes:
            task.notes = notes

    def delete_task(self, id: int):
        self.persistanceCtl.delete_task(id)

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
