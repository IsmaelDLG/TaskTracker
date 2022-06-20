from pathlib import Path
from time import time
from typing import List, Tuple

import shelve
from time import time

from tasktracker import getCustomLogger, CONFIG
from tasktracker.persistance.PersistanceCtlInt import PersistanceCtlInt
from tasktracker.persistance.model.task import Task


class ShelvePersistance(PersistanceCtlInt):
    def __init__(self):
        super().__init__()
        self.tasks_file = Path(CONFIG["SHELVE"]["tasks_file"])
        if not self.tasks_file.is_dir():

            self.taskDB = shelve.open(str(self.tasks_file))
            if not self.taskDB.get("_metadata"):
                self.taskDB["_metadata"] = {"last_id": 0}
        else:
            raise IsADirectoryError("Tasks database file is a directory!")

    def _update_metadata(self, key, value):
        meta = self.taskDB["_metadata"]
        meta[key] = value
        self.taskDB["_metadata"] = meta
        logger.debug("Updated metadata: {}".format(meta))

    def get_task_last_id(self) -> int:
        logger.debug("Last ID is: {}".format(self.taskDB["_metadata"]["last_id"]))
        meta = self.taskDB["_metadata"]
        return meta["last_id"]

    def get_task(self, id: int) -> Task:
        return self.taskDB[str(id)]

    def save_task(self, task: Task) -> Task:
        if not task.id:
            task.id = self.get_task_last_id()
            self._update_metadata("last_id", task.id + 1)

        self.taskDB[str(task.id)] = task

    def delete_task(self, id):
        task = self.taskDB[str(id)]
        logger.debug(":delete_task task: {task}")
        del self.taskDB[str(id)]


logger = getCustomLogger("persistance.ShelvePersistance")
