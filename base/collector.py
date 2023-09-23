from __future__ import annotations
from typing import Type, TYPE_CHECKING

if TYPE_CHECKING:
    from base import Context


class Collector:
    def __init__(self, context: Context) -> None:
        self.context = context

    @property
    def finished(self):
        return True

    def collect(self, line: str, no: int):
        raise NotImplementedError("extend it")


class CollectorsSet(set[Type[Collector]]):
    def build(self, ctx: Context):
        return set(map(lambda c: c(ctx), list(self)))

