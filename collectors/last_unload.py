from __future__ import annotations
from typing import Optional
from base import Collector


class LastUnloadLine(int):
    def __new__(cls, val: Optional[int] = None):
        return super(LastUnloadLine, cls).__new__(cls, val or -1)


class CollectLastUnload(Collector):
    finished = False

    def collect(self, line: str, no: int):
        if line.startswith('; CP TOOLCHANGE START'):
            self.context[LastUnloadLine] = LastUnloadLine(no)

        if line.startswith(';LAST UNLOAD REMOVED!!'):
            self.context[LastUnloadLine] = LastUnloadLine()
            self.finished = True
