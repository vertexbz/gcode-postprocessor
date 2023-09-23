from __future__ import annotations
from typing import Any
import argparse
from config import Config


def parse_args():
    parser = argparse.ArgumentParser(
        description="G-Code preprocessor"
    )

    # parser.add_argument('--dry-run', action='store_true', dest='dry_run')
    parser.add_argument(
        '-d', '--dry', '--dry-run',
        action='store_true', dest='dry_run',
        help='dry run - without modifying the file (default: False)'
    )
    parser.set_defaults(dry_run=False)

    parser.add_argument(
        '-f', '--feature',
        action='append',
        help='Use preprocessor feature',
        required=True
    )

    parser.add_argument('-v', '--verbose', action='count', default=0, help='increase verbosity')

    parser.add_argument('filename')
    return parser.parse_args()


def build_config(args: Any) -> Config:
    config = Config()
    config.dry_run = args.dry_run
    for feature in args.feature:
        config.feature.add(feature)

    return config


__all__ = ['build_config']
