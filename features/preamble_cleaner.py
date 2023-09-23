from __future__ import annotations
from typing import Optional
import re
from base import Processor, ProcessorsList, CollectorsSet, Context
from utils import match_z_only_move, match_xy_move
import logger

logger = logger.getChild('preamble_cleaner')


class ProcessPreamble(Processor):
    finished = False

    def process(self, context: Context, line: str, no: int) -> str:
        match = match_z_only_move(line)
        if match:
            logger.info(f'Fixing early Z only move [{no}]')
            return ""

        if re.search(r'^T[0-9]+\s*(?:;.+)?$', line, flags=re.IGNORECASE):
            logger.info(f'Initial tool change [{no}]')
            return ""

        match = match_xy_move(line)
        if match:
            self.finished = True

        return line


def load(_: CollectorsSet, processors: ProcessorsList, __: Optional[dict]) -> None:
    processors.append(ProcessPreamble)


__all__ = ['load']
