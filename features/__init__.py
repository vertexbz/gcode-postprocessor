from __future__ import annotations
from typing import Callable, Optional
import pkgutil
import importlib
from base import CollectorsSet, ProcessorsList
from config import Features
import logger

logger = logger.named_logger(__name__)

AVAILABLE_FEATURES: dict[str, Callable[[CollectorsSet, ProcessorsList, Optional[dict]], None]] = {}

__path__ = pkgutil.extend_path(__path__, __name__)
for imp, module, ispackage in pkgutil.iter_modules(path=__path__, prefix=__name__ + '.'):
    key = module.split('.')[-1]
    try:
        mod = importlib.import_module(module)
        AVAILABLE_FEATURES[key] = mod.load
        logger.debug(f'Registered feature "{key}"')
    except Exception as e:
        logger.critical(f'Failed loading feature "{key}":')
        raise e


def load_features(config: Features) -> tuple[CollectorsSet, ProcessorsList]:
    collectors = CollectorsSet()
    processors = ProcessorsList()

    if config.is_empty():
        logger.warn('No features selected')
        return collectors, processors

    for feature, feature_config in config.read():
        if feature not in AVAILABLE_FEATURES:
            logger.error(f'Unknown feature "{feature}"')
        else:
            try:
                AVAILABLE_FEATURES[feature](collectors, processors, feature_config)
                if feature_config:
                    logger.debug(f'Feature "{feature}" loaded with config: {feature_config}')
                else:
                    logger.debug(f'Feature "{feature}" loaded')
            except Exception as e:
                logger.critical(f'Failed loading feature "{feature}":')
                raise e

    return collectors, processors


__all__ = ['load_features']
