from __future__ import annotations
from typing import TYPE_CHECKING
from .collector import Collector
from .processor import Processor
from .context import Context

if TYPE_CHECKING:
    from gcode import Line


class Executor:
    def __init__(self, collectors: list[Collector], processors: list[Processor]) -> None:
        self.collectors = collectors
        self.processors = processors

    def execute(self, context: Context, lines: list[Line]):
        for i, line in enumerate(lines):
            finished = 0

            for collector in self.collectors:
                if not collector.finished:
                    collector.collect(context, line)
                if collector.finished:
                    finished = finished + 1

            if finished == len(self.collectors):
                break

        for i, _ in enumerate(lines):
            finished = 0

            for processor in self.processors:
                if not processor.finished:
                    processor.process(context, lines[i])
                if processor.finished:
                    finished = finished + 1

            if finished == len(self.processors):
                break
