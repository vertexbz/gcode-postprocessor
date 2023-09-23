from __future__ import annotations
import re
from base import Processor, ProcessorsList, CollectorsSet
from collectors.first_coordinate import CollectFirstCoordinate, FirstCoordinate
import logger

logger = logger.getChild('start_xy')


class ProcessStartXY(Processor):
    finished = False

    def process(self, line: str, no: int) -> str:
        if line.startswith("_PRINT_START"):
            if self.context[FirstCoordinate].x is None:
                raise RuntimeError("missing start x")
            if self.context[FirstCoordinate].y is None:
                raise RuntimeError("missing start y")

            if 'START_X=' in line:
                line = re.sub(r'START_X=\S*', f'START_X={self.context[FirstCoordinate].x.raw}', line)
                logger.info(f'START_X set to {self.context[FirstCoordinate].x.raw} [{no}]')
            if 'START_Y=' in line:
                line = re.sub(r'START_Y=\S*', f'START_Y={self.context[FirstCoordinate].y.raw}', line)
                logger.info(f'START_Y set to {self.context[FirstCoordinate].y.raw} [{no}]')

            self.finished = True

        return line


def load(collectors: CollectorsSet, processors: ProcessorsList) -> None:
    collectors.add(CollectFirstCoordinate)
    processors.append(ProcessStartXY)


__all__ = ['load']
