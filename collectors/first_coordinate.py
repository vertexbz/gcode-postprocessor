from __future__ import annotations
from typing import Optional
from base import Collector, Number
import utils as UTILS


class FirstCoordinate:
    x: Optional[Number] = None
    y: Optional[Number] = None


class CollectFirstCoordinate(Collector):
    @property
    def finished(self):
        return self.context[FirstCoordinate].x is not None and self.context[FirstCoordinate].y is not None

    def collect(self, line: str, no: int):
        match = UTILS.match_xy_move(line)
        if match:
            # Save the X and Y coordinates from the matched line
            self.context[FirstCoordinate].x = match[0]
            self.context[FirstCoordinate].y = match[1]
