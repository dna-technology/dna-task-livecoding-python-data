from abc import ABC, abstractmethod

from database import Database


class AbstractTransformer(ABC):
    def __init__(self, database: Database):
        self.conn = database.get_connection()

    @abstractmethod
    def transform(self, value: str):
        pass
