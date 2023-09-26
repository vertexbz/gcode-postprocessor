from __future__ import annotations
from typing import TYPE_CHECKING, Optional
from base import Processor, ProcessorsList, CollectorsSet, check_no_config
import logger
from gcode import match

if TYPE_CHECKING:
    from base import Context
    from gcode import Line

logger = logger.named_logger(__name__)


class ProcessMorningJumps(Processor):
    finished = False

    def process(self, context: Context, line: Line):
        if line.command is None:
            return

        if match.move(line, Z=True, X=False, Y=False, E=False):
            logger.info(f'Removing early Z only move [{line.no}]: {line}')
            line.clear()
            return

        if match.toolchange(line) is not None:
            logger.info(f'Removing initial tool change [{line.no}]: {line}')
            line.clear()
            return

        if match.move(line, X=True, Y=True):
            self.finished = True


def load(_: CollectorsSet, processors: ProcessorsList, config: Optional[dict]) -> None:
    check_no_config(logger, config)
    processors.append(ProcessMorningJumps)


__all__ = ['load']
