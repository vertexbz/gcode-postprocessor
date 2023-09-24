from __future__ import annotations
from typing import Optional
import re
from base import Processor, ProcessorsList, CollectorsSet, Context, check_no_config
from collectors.first_coordinate import CollectFirstCoordinate, FirstCoordinate
import logger

logger = logger.named_logger(__name__)


class ProcessStartXY(Processor):
    finished = False

    def process(self, context: Context, line: str, no: int) -> str:
        if line.startswith(self.config.macro.print_start):
            if context[FirstCoordinate].x is None:
                raise RuntimeError("missing start x")
            if context[FirstCoordinate].y is None:
                raise RuntimeError("missing start y")

            if 'START_X=' in line:
                line = re.sub(r'START_X=\S*', f'START_X={context[FirstCoordinate].x.raw}', line)
                logger.info(f'START_X set to {context[FirstCoordinate].x.raw} [{no}]')
            if 'START_Y=' in line:
                line = re.sub(r'START_Y=\S*', f'START_Y={context[FirstCoordinate].y.raw}', line)
                logger.info(f'START_Y set to {context[FirstCoordinate].y.raw} [{no}]')

            self.finished = True

        return line


def load(collectors: CollectorsSet, processors: ProcessorsList, config: Optional[dict]) -> None:
    check_no_config(logger, config)
    collectors.add(CollectFirstCoordinate)
    processors.append(ProcessStartXY)


__all__ = ['load']
