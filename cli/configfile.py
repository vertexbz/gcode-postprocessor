from __future__ import annotations
from typing import Union
from config import Config, Macros, Features
import logger
import yaml

logger = logger.getChild('configfile')


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


def apply_features(data: list, config: Features):
    if not isinstance(data, list):
        logger.error(f'Invalid feature configuration "{data}"')
        raise logger.SilentError()

    for entry in data:
        if isinstance(entry, str):
            config.add(entry)
        elif isinstance(entry, list) and len(entry) == 1 and isinstance(entry[0], str):
            config.add(entry[0])
        elif isinstance(entry, list) and len(entry) == 2 and isinstance(entry[0], str) and isinstance(entry[1], dict):
            config.add(entry[0], entry[1])
        else:
            logger.error(f'Invalid feature configuration "{entry}"')
            raise logger.SilentError()


def apply_root(data: dict, config: Config):
    apply(apply_features, data.pop('feature', []), config.feature)
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
