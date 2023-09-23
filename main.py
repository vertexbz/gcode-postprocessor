from __future__ import annotations
from cli.config import build_config, parse_args
from config import Config
from base.context import Context
from base.executor import Executor
from features import load_features
import logger


def process(ctx: Context, config: Config, input_file: str):
    logger.debug('Loading features...')
    collectors, processors = load_features(config.feature)

    logger.debug('Building postprocessor...')
    executor = Executor(collectors.build(ctx), processors.build(ctx))

    logger.debug(f'Loading "{input_file}"')
    with open(input_file, "r") as f:
        lines = f.readlines()

    logger.debug('Processing...')
    executor.execute(lines)

    if not config.dry_run:
        logger.debug('Saving')
        with open(input_file, "w") as f:
            f.writelines(lines)

    logger.info(f'Finished processing "{input_file}"')


if __name__ == '__main__':
    args = parse_args()
    config = build_config(args)
    ctx = Context()

    if args.verbose > 2:
        logger.setLevel(logger.DEBUG)
    elif args.verbose > 1:
        logger.setLevel(logger.INFO - 1)
    elif args.verbose > 0:
        logger.setLevel(logger.INFO)

    process(ctx, config, args.filename)
