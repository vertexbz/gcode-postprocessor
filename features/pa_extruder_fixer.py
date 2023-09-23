from __future__ import annotations
import re
from base import Processor, ProcessorsList, CollectorsSet
import logger

logger = logger.getChild('pa_extruder_fixer')


class ProcessSetPressureAdvance(Processor):
    finished = False

    def process(self, line: str, no: int) -> str:
        if line.startswith("SET_PRESSURE_ADVANCE"):
            if 'EXTRUDER=' in line:
                logger.info(f'Fixing SET_PRESSURE_ADVANCE EXTRUDER= parameter [{no}]')
                line = re.sub(r'\s+EXTRUDER=\S*', '', line)

        return line


def load(collectors: CollectorsSet, processors: ProcessorsList) -> None:
    processors.append(ProcessSetPressureAdvance)


__all__ = ['load']
