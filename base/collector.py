from __future__ import annotations
from typing import Type, TYPE_CHECKING

if TYPE_CHECKING:
    from base import Context
    from base.config import Config


class Collector:
    def __init__(self, config: Config) -> None:
        self.config = config

    @property
    def finished(self):
        return True

    def collect(self, context: Context, line: str, no: int):
        raise NotImplementedError("extend it")


class CollectorsSet(set[Type[Collector]]):
    def build(self, config: Config):
        return set(map(lambda c: c(config), list(self)))
