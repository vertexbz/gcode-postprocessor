from __future__ import annotations
import re
from base import Processor, ProcessorsList, CollectorsSet
from collectors.last_unload import CollectLastUnload, LastUnloadLine
from utils import match_retraction
import logger

logger = logger.getChild('no_final_unload')


class ProcessFinalUpload(Processor):
    finished = False
    almost_finished = False
    last_wipe = False

    def process(self, line: str, no: int) -> str:
        if self.context[LastUnloadLine] <= 0:
            self.finished = True
            return line

        if line.startswith("_PRINT_START"):
            line = re.sub(r'\s+MMU_NO_FINAL_UNLOAD=\S*', '', line)
            line = f'{line} MMU_NO_FINAL_UNLOAD=1'
            logger.info('Ensured MMU_NO_FINAL_UNLOAD=1 in print start macro')
            return line

        if no >= self.context[LastUnloadLine] - 15:
            if match_retraction(line):
                self.last_wipe = True

        if self.last_wipe or no >= self.context[LastUnloadLine] - 1:
            if self.almost_finished:
                self.finished = True
                return ";LAST UNLOAD REMOVED!!"

            if line.startswith('; CP TOOLCHANGE END'):
                self.almost_finished = True

            logger.info(f'Removing final unload G-Code [{no}]: {line.rstrip()}')
            return ""

        return line


def load(collectors: CollectorsSet, processors: ProcessorsList) -> None:
    collectors.add(CollectLastUnload)
    processors.append(ProcessFinalUpload)


__all__ = ['load']
