from __future__ import annotations
import re
from base import Collector, Number


class PrintSection:
    tool: int = -1
    start_line: int = -1
    end_line: int = -1
    type: str = ""
    z: Number = Number('0')

    def __init__(self, tool: int, type: str, z: Number, start_line: int, end_line: int):
        self.tool = tool
        self.type = type
        self.z = z
        self.start_line = start_line
        self.end_line = end_line

    def __str__(self):
        return f'T{self.tool} ; {self.z.raw}mm [{self.start_line}:{self.end_line}] {self.type}'

    def __repr__(self):
        return f'T{self.tool} ; {self.z.raw}mm [{self.start_line}:{self.end_line}] {self.type}'


class PrintSections(list[PrintSection]):
    pass


class CollectSections(Collector):
    finished = False

    _current_type = ""
    _current_tool = -1
    _current_z = Number('0')
    _first_extrude_line = -1
    _last_extrude_line = -1

    def _line_changed(self, no: int):
        if self._current_type != "" and self._first_extrude_line == -1:
            self._first_extrude_line = no

        self._last_extrude_line = no

    def _tool_changed(self, new_tool: int):
        if self._current_tool != new_tool:
            self.add_section()
            self._current_tool = new_tool

    def _z_changed(self, new_z: Number):
        if self._current_z.raw != new_z.raw:
            self.add_section()
            self._current_z = new_z

    def _type_changed(self, new_type: str):
        if new_type == "Custom":
            return

        if self._current_type != new_type:
            self.add_section()
            self._current_type = new_type

    def add_section(self):
        if self._current_type in ('', 'Custom'):
            return
        if self._first_extrude_line == -1:
            return
        if self._last_extrude_line == -1:
            return

        self.context[PrintSections].append(
            PrintSection(
                self._current_tool,
                self._current_type,
                self._current_z,
                self._first_extrude_line,
                self._last_extrude_line
            )
        )

        self._first_extrude_line = -1
        self._last_extrude_line = -1

    def collect(self, line: str, no: int):
        if line.startswith("_PRINT_START"):
            match = re.match(r'INITIAL_TOOL=(\d+)', line)
            if match:
                self._current_tool = int(match.group(1))
                return

        if line.startswith("T"):
            match = re.match(r'T(\d+)', line)
            if match:
                new_tool = int(match.group(1))
                self._tool_changed(new_tool)
                return

        if line.startswith(";TYPE:"):
            self._type_changed(line[6:].rstrip())
            return

        if line.startswith(";Z:"):
            height = line[3:].rstrip()
            self._z_changed(Number(height))
            return

        if line.startswith("G0 ") or line.startswith("G1 "):
            if ' E' in line:
                self._line_changed(no)
