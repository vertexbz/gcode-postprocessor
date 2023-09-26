from __future__ import annotations
from typing import TYPE_CHECKING, Optional
from base import Collector
from gcode import match

if TYPE_CHECKING:
    from base import Context
    from gcode import Line


class FirstCoordinate:
    x: Optional[float] = None
    y: Optional[float] = None


class CollectFirstCoordinate(Collector):
    finished = False

    def collect(self, context: Context, line: Line):
        if match.move(line, X=True, Y=True):
            # Save the X and Y coordinates from the matched line
            context[FirstCoordinate].x = line.params.X
            context[FirstCoordinate].y = line.params.Y
            self.finished = True
