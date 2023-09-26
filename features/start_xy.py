from __future__ import annotations
from typing import TYPE_CHECKING, Optional
from base import Processor, ProcessorsList, CollectorsSet, check_no_config
from collectors.first_coordinate import CollectFirstCoordinate, FirstCoordinate
import logger

if TYPE_CHECKING:
    from base import Context
    from gcode import Line

logger = logger.named_logger(__name__)


class ProcessStartXY(Processor):
    finished = False

    def process(self, context: Context, line: Line):
        if line.command == self.config.macro.print_start:
            if context[FirstCoordinate].x is None:
                raise RuntimeError("missing start x")
            if context[FirstCoordinate].y is None:
                raise RuntimeError("missing start y")

            line.params.START_X = context[FirstCoordinate].x
            line.params.START_Y = context[FirstCoordinate].y
            logger.info(f'Start coordinates set to {context[FirstCoordinate].x}, {context[FirstCoordinate].y} [{line.no}]: {line}')

            self.finished = True


def load(collectors: CollectorsSet, processors: ProcessorsList, config: Optional[dict]) -> None:
    check_no_config(logger, config)
    collectors.add(CollectFirstCoordinate)
    processors.append(ProcessStartXY)


__all__ = ['load']
