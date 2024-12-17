from abc import ABC, abstractmethod


class AbstractTransformer(ABC):
    @abstractmethod
    def transform(self, key: str | None, value: str):
        pass