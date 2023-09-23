from __future__ import annotations
from typing import Callable
import pkgutil
import importlib
from base import CollectorsSet, ProcessorsList
from config import Features
import logger

AVAILABLE_FEATURES: dict[str, Callable[[CollectorsSet, ProcessorsList], None]] = {}

__path__ = pkgutil.extend_path(__path__, __name__)


def init():
    if len(AVAILABLE_FEATURES) > 0:
        return

    for imp, module, ispackage in pkgutil.iter_modules(path=__path__, prefix=__name__ + '.'):
        key = module.split('.')[-1]
        try:
            mod = importlib.import_module(module)
            AVAILABLE_FEATURES[key] = mod.load
            logger.debug(f'registered feature "{key}"')
        except Exception as e:
            logger.critical(f'failed loading feature "{key}":')
            raise e


def load_features(config: Features) -> tuple[CollectorsSet, ProcessorsList]:
    init()

    collectors = CollectorsSet()
    processors = ProcessorsList()

    if config.is_empty():
        logger.warn('no features selected')
        return collectors, processors

    for feature in config.read():
        if feature not in AVAILABLE_FEATURES:
            logger.error(f'invalid feature "{feature}"')
        else:
            try:
                AVAILABLE_FEATURES[feature](collectors, processors)
                logger.debug(f'feature "{feature} loaded')
            except Exception as e:
                logger.critical(f'failed loading feature "{key}":')
                raise e

    return collectors, processors
