from __future__ import annotations
from .collector import Collector
from .processor import Processor


class Executor:
    def __init__(self, collectors: list[Collector], processors: list[Processor]) -> None:
        self.collectors = collectors
        self.processors = processors

    def execute(self, lines: list[str]):
        for i, line in enumerate(lines):
            finished = 0

            for collector in self.collectors:
                if not collector.finished:
                    collector.collect(line, i)
                if collector.finished:
                    finished = finished + 1

            if finished == len(self.collectors):
                break

        for i, _ in enumerate(lines):
            finished = 0

            for processor in self.processors:
                if not processor.finished:
                    lines[i] = processor.process(lines[i], i)
                if processor.finished:
                    finished = finished + 1

            if finished == len(self.processors):
                break
