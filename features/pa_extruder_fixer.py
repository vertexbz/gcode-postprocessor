from __future__ import annotations
from typing import Optional
import re
from base import Processor, ProcessorsList, CollectorsSet, Context, check_no_config
import logger

logger = logger.named_logger(__name__)


class ProcessSetPressureAdvance(Processor):
    finished = False

    def process(self, context: Context, line: str, no: int) -> str:
        if line.startswith("SET_PRESSURE_ADVANCE"):
            if 'EXTRUDER=' in line:
                logger.info(f'Fixing SET_PRESSURE_ADVANCE EXTRUDER= parameter [{no}]')
                line = re.sub(r'\s+EXTRUDER=\S*', '', line)

        return line


def load(_: CollectorsSet, processors: ProcessorsList, config: Optional[dict]) -> None:
    check_no_config(logger, config)
    processors.append(ProcessSetPressureAdvance)


__all__ = ['load']
