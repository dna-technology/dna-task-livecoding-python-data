from abc import ABC, abstractmethod

from abstract_database import AbstractDatabase


class AbstractTransformer(ABC):
    def __init__(self, database: AbstractDatabase):
        self.conn = database.get_connection()

    @abstractmethod
    def transform(self, value: str):
        pass
