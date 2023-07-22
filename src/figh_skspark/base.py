from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ConfigStorage(ABC, Generic[T], BaseModel):
    @abstractmethod
    def get(self, version: str = "latest") -> T:
        """returns configuration of the version"""
