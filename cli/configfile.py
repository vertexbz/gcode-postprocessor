from __future__ import annotations
from typing import Union, Optional
from config import Config, Macros, Features
import error
import logger
import yaml

logger = logger.named_logger(__name__)


def pop(data: dict, key: str, default = None):
    if key in data:
        return data.pop(key)

    keyParts = key.split('_')

    key = '-'.join(keyParts)
    if key in data:
        return data.pop(key)

    key = ''.join(map(lambda e: e[1] if e[0] == 0 else e[1].title(), enumerate(keyParts)))
    if key in data:
        return data.pop(key)

    key = ''.join(keyParts)
    if key in data:
        return data.pop(key)

    return default


def apply_macros(data: dict, config: Macros):
    keys = list(filter(lambda k: not k.startswith('_'), dir(config)))
    for key in keys:
        setattr(config, key, pop(data, key, getattr(config, key)))


def apply_features(data: Optional[list], config: Features):
    if data is None:
        return

    if not isinstance(data, list):
        logger.error(f'Invalid feature configuration "{data}"')
        raise error.SilentError()

    config.clear()

    for entry in data:
        if isinstance(entry, str):
            config.add(entry)
        elif isinstance(entry, dict) and len(entry) == 1:
            config.add(list(entry.keys())[0], list(entry.values())[0])
        else:
            logger.error(f'Invalid feature configuration "{entry}"')
            raise error.SilentError()


def apply_root(data: dict, config: Config):
    apply(apply_features, data.pop('feature', None), config.feature)
    apply(apply_macros, data.pop('macro', {}), config.macro)

    config.dry_run = pop(data, 'dry_run', config.dry_run)


def load_yaml(filepath: str) -> dict:
    with open(filepath, 'r', encoding='utf-8') as stream:
        return yaml.safe_load(stream)


def check_invalid(data: Union[dict, list]):
    if isinstance(data, list):
        return

    for key in data.keys():
        logger.error(f'Invalid configuration key "{key}"')


def apply(fn, data: dict, config: Config):
    fn(data, config)
    check_invalid(data)


def apply_config_from_file(filepath: str, config: Config) -> None:
    logger.debug(f'Loading "{filepath}"')
    apply(apply_root, load_yaml(filepath), config)
