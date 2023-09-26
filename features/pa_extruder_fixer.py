from __future__ import annotations
from typing import TYPE_CHECKING, Optional
from base import Processor, ProcessorsList, CollectorsSet, check_no_config
import logger

if TYPE_CHECKING:
    from base import Context
    from gcode import Line

logger = logger.named_logger(__name__)


class ProcessSetPressureAdvance(Processor):
    finished = False

    def process(self, context: Context, line: Line):
        if line.command == "SET_PRESSURE_ADVANCE":
            if 'EXTRUDER' in line.params:
                logger.info(f'Removing SET_PRESSURE_ADVANCE EXTRUDER= parameter [{line.no}]: {line}')
                del line.params.EXTRUDER


def load(_: CollectorsSet, processors: ProcessorsList, config: Optional[dict]) -> None:
    check_no_config(logger, config)
    processors.append(ProcessSetPressureAdvance)


__all__ = ['load']
