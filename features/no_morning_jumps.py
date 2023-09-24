from __future__ import annotations
from typing import Optional
import re
from base import Processor, ProcessorsList, CollectorsSet, Context, check_no_config
from utils import match_z_only_move, match_xy_move
import logger

logger = logger.named_logger(__name__)


class ProcessMorningJumps(Processor):
    finished = False

    def process(self, context: Context, line: str, no: int) -> str:
        match = match_z_only_move(line)
        if match:
            logger.info(f'Removing early Z only move [{no}]: {line.rstrip()}')
            return ""

        if re.search(r'^T[0-9]+\s*(?:;.+)?$', line, flags=re.IGNORECASE):
            logger.info(f'Removing initial tool change [{no}]: {line.rstrip()}')
            return ""

        match = match_xy_move(line)
        if match:
            self.finished = True

        return line


def load(_: CollectorsSet, processors: ProcessorsList, config: Optional[dict]) -> None:
    check_no_config(logger, config)
    processors.append(ProcessMorningJumps)


__all__ = ['load']
