from __future__ import annotations
from typing import Type, Generic, TypeVar, TYPE_CHECKING

if TYPE_CHECKING:
    from base import Context
    from base.config import Config


class Processor:
    def __init__(self, config: Config) -> None:
        self.config = config

    @property
    def finished(self):
        return True

    def process(self, context: Context, line: str, no: int) -> str:
        raise NotImplementedError("extend it")


class ProcessorsList(list[Type[Processor]]):
    def build(self, config: Config) -> list[Processor]:
        return list(map(lambda p: p(config), self))


T = TypeVar('T')


class ConfigurableProcessor(Processor, Generic[T]):
    def __init__(self, config: Config, feature_config: T) -> None:
        super().__init__(config)
        self.feature_config: T = feature_config

