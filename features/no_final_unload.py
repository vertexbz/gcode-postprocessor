from __future__ import annotations
from typing import Optional
import re
from base import Processor, ProcessorsList, CollectorsSet, Context, check_no_config
from collectors.last_unload import CollectLastUnload, LastUnloadLine
from utils import match_retraction
import logger

logger = logger.named_logger(__name__)


class ProcessFinalUpload(Processor):
    finished = False
    almost_finished = False
    last_wipe = False

    def process(self, context: Context, line: str, no: int) -> str:
        if context[LastUnloadLine] <= 0:
            self.finished = True
            return line

        if line.startswith(self.config.macro.print_start):
            line = re.sub(r'\s+MMU_NO_FINAL_UNLOAD=\S*', '', line)
            line = f'{line.rstrip()} MMU_NO_FINAL_UNLOAD=1\n'
            logger.info('Ensured MMU_NO_FINAL_UNLOAD=1 in print start macro')
            return line

        if no >= context[LastUnloadLine] - 15:
            if match_retraction(line):
                self.last_wipe = True

        if self.last_wipe or no >= context[LastUnloadLine] - 1:
            if line.startswith('; stop printing object'):
                return line

            if self.almost_finished:
                self.finished = True
                return ";LAST UNLOAD REMOVED!!"

            if line.startswith('; CP TOOLCHANGE END'):
                self.almost_finished = True

            logger.info(f'Removing final unload G-Code [{no}]: {line.rstrip()}')
            return ""

        return line


def load(collectors: CollectorsSet, processors: ProcessorsList, config: Optional[dict]) -> None:
    check_no_config(logger, config)
    collectors.add(CollectLastUnload)
    processors.append(ProcessFinalUpload)


__all__ = ['load']
