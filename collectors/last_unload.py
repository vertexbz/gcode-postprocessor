from __future__ import annotations
from typing import TYPE_CHECKING, Optional
from base import Collector

if TYPE_CHECKING:
    from base import Context
    from gcode import Line


class LastUnloadLine(int):
    def __new__(cls, val: Optional[int] = None):
        return super(LastUnloadLine, cls).__new__(cls, val or -1)


class CollectLastUnload(Collector):
    finished = False

    def collect(self, context: Context, line: Line):
        if line.comment == 'CP TOOLCHANGE START':
            context[LastUnloadLine] = LastUnloadLine(line.no)

        if line.comment == 'LAST UNLOAD REMOVED!!':
            context[LastUnloadLine] = LastUnloadLine()
            self.finished = True
