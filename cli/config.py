from __future__ import annotations

import os.path
from typing import Any, Optional
import argparse
import re
import json
from .configfile import apply_config_from_file
from .keyvalue import KeyValue
from config import Config
import const as CONST
import logger

def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return open(arg, 'r')  # return an open file handle


def parse_args():
    parser = argparse.ArgumentParser(
        description="G-Code preprocessor"
    )

    parser.add_argument(
        '-d', '--dry', '--dry-run',
        action='store_true', dest='dry_run', default=False,
        help='dry run - without modifying the file (default: False)'
    )

    parser.add_argument(
        "-c", "--config",
        dest="config", help="custom default configuration file", metavar="CONFIG_FILE",
        type=lambda x: is_valid_file(parser, x)
    )

    parser.add_argument(
        '-f', '--feature',
        action='append', dest='features',
        help='use preprocessor feature',
    )

    parser.add_argument('-m', '--macro', dest='macros', default={}, action=KeyValue, help="set macro name as key=value pair", metavar="MACRO=CUSTOM")
    parser.add_argument('-v', '--verbose', action='count', default=0, help='increase verbosity')

    parser.add_argument('filename',  help="input G-Code file", metavar="INPUT_FILE")
    return parser.parse_args()


def parse_feature_string(feature_string: str) -> tuple[str, str]:
    split = feature_string.split('=', 1)

    if len(split) == 2:
        return split[0], split[1]

    return split[0], ''


def build_feature_config_dict(feature: str, config_string: str) -> Optional[dict]:
    if len(config_string) > 0:
        # We'll start by removing any extraneous white spaces
        config_string = re.sub(r'\s', '', config_string)

        # Surrounding any word with "
        config_string = re.sub(r'(\w+)', '"\g<1>"', config_string)

        # Replacing = with :
        config_string = re.sub('=', ':', config_string)

        try:
            return json.loads('{' + config_string + '}')
        except Exception:
            logger.error(f'Invalid configuration provided for feature "{feature}", "{config_string}" is not a valid feature configuration')
            raise logger.SilentError()

    return None


def build_config(args: Any) -> Config:
    config = Config()

    # Load defaults
    apply_config_from_file(os.path.join(CONST.SRCDIR, 'config.default.yaml'), config)

    # Load custom defaults
    config_file = os.path.join(CONST.SRCDIR, 'config.yaml')
    if not os.path.exists(config_file):
        config_file = os.path.join(CONST.SRCDIR, 'config.yml')
    if os.path.exists(config_file):
        apply_config_from_file(config_file, config)

    # Load custom CLI defaults
    if args.config:
        apply_config_from_file(args.config.name, config)

    # Apply CLI params
    config.dry_run = args.dry_run
    for feature_string in args.features:
        feature, config_string = parse_feature_string(feature_string)
        config.feature.add(feature, build_feature_config_dict(feature, config_string))

    for key, value in args.macros.items():
        key = key.lower()
        if not hasattr(config.macro, key):
            logger.error(f'Invalid macro "{key}"')
        else:
            setattr(config.macro, key, value)

    if args.verbose > 2:
        config.log_level = logger.DEBUG
    elif args.verbose > 1:
        config.log_level = logger.INFO - 1
    elif args.verbose > 0:
        config.log_level = logger.INFO

    return config


def get_config_and_filepath() -> tuple[Config, str]:
    args = parse_args()

    config = build_config(args)

    return config, args.filename


def get_config() -> Config:
    return build_config(parse_args())


__all__ = ['get_config', 'get_config_and_filepath']
