from __future__ import annotations
from typing import Type, Optional, TypeVar, TYPE_CHECKING
import logger

if TYPE_CHECKING:
    from .processor import ConfigurableProcessor


C = TypeVar('C')


def bind_config(processor: Type[ConfigurableProcessor[C]], feature_config: C):
    if not feature_config:
        return processor

    return lambda config: processor(config, feature_config)


def check_no_config(logger: logger.Logger, config: Optional[dict]):
    if config:
        logger.error('Unexpected configuration. Ignored.')
