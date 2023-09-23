from __future__ import annotations
from typing import Type, TYPE_CHECKING

if TYPE_CHECKING:
    from base import Context


class Processor:
    def __init__(self, context: Context) -> None:
        self.context = context

    @property
    def finished(self):
        return True

    def process(self, line: str, no: int) -> str:
        raise NotImplementedError("extend it")


class ProcessorsList(list[Type[Processor]]):
    def build(self, ctx: Context) -> list[Processor]:
        return list(map(lambda p: p(ctx), self))
