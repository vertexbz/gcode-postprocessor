from __future__ import annotations
from typing import TYPE_CHECKING, Optional
from base import Processor, ProcessorsList, CollectorsSet, check_no_config
from collectors.last_unload import CollectLastUnload, LastUnloadLine
from gcode import match
import logger

if TYPE_CHECKING:
    from base import Context
    from gcode import Line

logger = logger.named_logger(__name__)


class ProcessFinalUpload(Processor):
    finished = False
    almost_finished = False
    last_wipe = False

    def process(self, context: Context, line: Line):
        if context[LastUnloadLine] <= 0:
            self.finished = True
            return

        if line.command == self.config.macro.print_start:
            line.params.MMU_NO_FINAL_UNLOAD = 1
            logger.info(f'Ensured MMU_NO_FINAL_UNLOAD=1 in print start macro [{line.no}]: {line}')
            return

        if line.no >= context[LastUnloadLine] - 15:
            if (match.move(line, E=True) and line.params.E < 0) or line.command == 'G10':
                self.last_wipe = True

        if self.last_wipe or line.no >= context[LastUnloadLine] - 1:
            if line.comment is not None and line.comment.startswith('stop printing object'):
                return
            if line.command is not None and line.command.startswith('EXCLUDE_OBJECT_'):
                return

            logger.info(f'Removing final unload G-Code [{line.no}]: {line}')
            if self.almost_finished:
                self.finished = True
                line.remove()
                line.comment = 'LAST UNLOAD REMOVED!!'
                return

            if line.comment is not None and line.comment.startswith('CP TOOLCHANGE END'):
                self.almost_finished = True

            line.remove()


def load(collectors: CollectorsSet, processors: ProcessorsList, config: Optional[dict]) -> None:
    check_no_config(logger, config)
    collectors.add(CollectLastUnload)
    processors.append(ProcessFinalUpload)


__all__ = ['load']
