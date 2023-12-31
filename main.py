from __future__ import annotations
import sys
from cli.config import get_config_and_filepath
from base.config import Config
from base import SilentError, Context, Executor
from features import load_features
from gcode import Line
import logger
import const


def process(ctx: Context, config: Config, input_file: str):
    logger.debug('Loading features...')
    collectors, processors = load_features(config.feature)

    logger.debug('Building postprocessor...')
    executor = Executor(collectors.build(config), processors.build(config))

    logger.debug(f'Loading "{input_file}"')
    with open(input_file, "r") as f:
        lines = f.readlines()

    lines = list(map(lambda e: Line(e[1], e[0]), enumerate(lines)))

    logger.debug('Processing...')
    executor.execute(ctx, lines)

    if not config.dry_run:
        logger.debug('Saving')
        with open(input_file, "w") as f:
            f.writelines(list(map(lambda l: l.raw, lines)))

    logger.info(f'Finished processing "{input_file}"')


if __name__ == '__main__':
    logger.info('G-Code Postprocessor')
    logger.named_logger('env').debug(f'Src dir: {const.SRCDIR}')
    logger.named_logger('env').debug(f'V-Env dir: {const.VENVDIR}')

    try:
        try:
            config, filepath = get_config_and_filepath()
            logger.set_level(config.log_level)
        except Exception as e:
            logger.set_level(logger.ERROR)
            raise e

        logger.named_logger('env').debug(f'DRY RUN: {config.dry_run}')

        process(Context(), config, filepath)
    except Exception as e:
        if not isinstance(e, SilentError):
            raise e
        else:
            sys.exit(1)
