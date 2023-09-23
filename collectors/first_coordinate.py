from __future__ import annotations
from typing import Optional
from base import Collector, Number, Context
from utils import match_xy_move


class FirstCoordinate:
    x: Optional[Number] = None
    y: Optional[Number] = None


class CollectFirstCoordinate(Collector):
    finished = False

    def collect(self, context: Context, line: str, no: int):
        match = match_xy_move(line)
        if match:
            # Save the X and Y coordinates from the matched line
            context[FirstCoordinate].x = match[0]
            context[FirstCoordinate].y = match[1]
            self.finished = True
