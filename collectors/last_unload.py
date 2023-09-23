from __future__ import annotations
from typing import Optional
from base import Collector, Context


class LastUnloadLine(int):
    def __new__(cls, val: Optional[int] = None):
        return super(LastUnloadLine, cls).__new__(cls, val or -1)


class CollectLastUnload(Collector):
    finished = False

    def collect(self, context: Context, line: str, no: int):
        if line.startswith('; CP TOOLCHANGE START'):
            context[LastUnloadLine] = LastUnloadLine(no)

        if line.startswith(';LAST UNLOAD REMOVED!!'):
            context[LastUnloadLine] = LastUnloadLine()
            self.finished = True
