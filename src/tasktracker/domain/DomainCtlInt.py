import abc
from typing import List, Tuple
from tasktracker.persistance.model.task import Task


class DomainCtlInt(abc.ABC):
    @abc.abstractclassmethod
    def create_task(
        self,
        creation_time: float,
        start_time: float,
        end_time: float,
        pause_time: float,
        tags: Tuple[str],
        notes: str,
    ) -> Task:
        pass

    @abc.abstractclassmethod
    def get_task(self, id: int):
        pass

    @abc.abstractclassmethod
    def edit_task(self, start_time, end_time, pause, tags, notes):
        pass

    @abc.abstractclassmethod
    def delete_task(self, id: int):
        pass
