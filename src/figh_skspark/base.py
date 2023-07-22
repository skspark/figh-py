from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from pydantic import BaseModel

VERSION_LATEST = "latest"

T = TypeVar("T")


class ConfigStorage(ABC, Generic[T]):
    @abstractmethod
    def get(self, version: str = VERSION_LATEST) -> T:
        """returns configuration of the version"""
