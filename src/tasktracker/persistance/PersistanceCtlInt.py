from typing import List, Tuple
import abc
from tasktracker.persistance.model.task import Task


class PersistanceCtlInt(abc.ABC):
    @abc.abstractclassmethod
    def save_task(self, task: Task) -> Task:
        pass

    @abc.abstractclassmethod
    def delete_task(self):
        pass

    @abc.abstractclassmethod
    def get_task(self):
        pass
