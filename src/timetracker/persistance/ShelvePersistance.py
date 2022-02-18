from pathlib import Path
from time import time
from typing import List, Tuple

import shelve
from time import time

from persistance.PersistanceCtlInt import PersistanceCtlInt
from persistance.model.task import Task


class ShelvePersistance(PersistanceCtlInt):
    def __init__(self, config):
        super().__init__()
        self.tasks_file = Path(config["tasks_file"])
        if not self.tasks_file.is_dir():

            self.taskDB = shelve.open(str(self.tasks_file))
            if not self.taskDB.get("_metadata"):
                self.taskDB["_metadata"] = {"last_id": 0}
        else:
            raise IsADirectoryError("Tasks database file is a directory!")

        self.profiles_file = Path(config["profiles_file"])
        if not self.profiles_file.is_dir():
            self.profileDB = shelve.open(str(self.profiles_file))
            if not self.profileDB.get("_metadata"):
                self.profileDB["_metadata"] = {"last_id": 0}
        else:
            raise IsADirectoryError("Profiles database file is a directory!")

    def create_task(
        self,
        creation_time: float,
        start_time: float,
        end_time: float,
        pause_time: float,
        tags: Tuple[str],
        notes: str,
    ) -> Task:
        last_id = self.get_task_last_id()
        newtask = Task(
            last_id + 1,
            creation_time,
            start_time,
            end_time,
            pause_time,
            tags,
            notes,
        )

        self._update_metadata("last_id", last_id + 1)
        self.taskDB[str(newtask.id)] = newtask

        return newtask

    def _update_metadata(self, key, value):
        meta = self.taskDB["_metadata"]
        meta[key] = value
        self.taskDB["_metadata"] = meta
        print("Updated metadata: {}".format(meta))

    def get_task_last_id(self) -> int:
        print("Last ID is: {}".format(self.taskDB["_metadata"]["last_id"]))
        meta = self.taskDB["_metadata"]
        return meta["last_id"]

    def get_task(self, id: int) -> Task:
        return self.taskDB[str(id)]

    def save_changes(self, tasks=True, profiles=True) -> None:
        if tasks:
            self.taskDB.sync()
        if profiles:
            self.taskDB.sync()
