from __future__ import annotations

import sys

from cli.config import get_config_and_filepath
from config import Config
from base.context import Context
from base.executor import Executor
from features import load_features
import logger
import const as CONST

def process(ctx: Context, config: Config, input_file: str):
    logger.debug('Loading features...')
    collectors, processors = load_features(config.feature)

    logger.debug('Building postprocessor...')
    executor = Executor(collectors.build(config), processors.build(config))

    logger.debug(f'Loading "{input_file}"')
    with open(input_file, "r") as f:
        lines = f.readlines()

    logger.debug('Processing...')
    executor.execute(ctx, lines)

    if not config.dry_run:
        logger.debug('Saving')
        with open(input_file, "w") as f:
            f.writelines(lines)

    logger.info(f'Finished processing "{input_file}"')


if __name__ == '__main__':
    logger.debug(f'Src dir: {CONST.SRCDIR}')
    logger.debug(f'V-Env dir: {CONST.VENVDIR}')

    try:
        try:
            config, filepath = get_config_and_filepath()
            logger.setLevel(config.log_level)
        except Exception as e:
            logger.setLevel(logger.ERROR)
            raise e

        logger.debug(f'DRY RUN: {config.dry_run}')

        process(Context(), config, filepath)
    except Exception as e:
        if not isinstance(e, logger.SilentError):
            raise e
        else:
            sys.exit(1)
