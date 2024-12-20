from abc import ABC, abstractmethod
from sqlite3 import Connection


class AbstractDatabase(ABC):

    @abstractmethod
    def get_connection(self) -> Connection:
        pass
