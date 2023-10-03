from __future__ import annotations
from typing import TYPE_CHECKING, Optional, Union
from base import Collector
from gcode import parse_parameter, match

if TYPE_CHECKING:
    from base import Context
    from gcode import Line


class Tool(int):
    def __new__(cls, val: Optional[int] = None):
        return None if val is None or val < 0 else super(Tool, cls).__new__(cls, val)


class Z(float):
    def __new__(cls, val: Optional[Union[int,float]] = None):
        return None if val is None or val < 0 else super(Z, cls).__new__(cls, val)


class Type(str):
    def __new__(cls, val: Optional[str] = None):
        return None if val is None or val.lower() in ('', 'custom') else super(Type, cls).__new__(cls, val.lower())


class PrintSection:
    tool: Tool = -1
    start_line: int = -1
    end_line: int = -1
    type: Type = ''
    z: Z = 0

    def __init__(self, tool: int, type: str, z: float, start_line: int, end_line: int):
        self.tool = Tool(tool)
        self.type = Type(type)
        self.z = Z(z)
        self.start_line = start_line
        self.end_line = end_line

    def __str__(self):
        return f'T{self.tool} ; {self.z}mm [{self.start_line}:{self.end_line}] {self.type}'

    def __repr__(self):
        return f'T{self.tool} ; {self.z}mm [{self.start_line}:{self.end_line}] {self.type}'


class PrintSections(list[PrintSection]):
    pass


class PrintInfo:
    def __init__(self):
        self.used_tools: set[Tool] = set()

    def __str__(self):
        return '\n'.join([
            f'Used tools: {self.used_tools}',
        ])

    def __repr__(self):
        return str(self)


class CollectSections(Collector):
    finished = False

    _current_type = ""
    _current_tool = -1
    _current_z = 0.0
    _first_extrude_line = -1
    _last_extrude_line = -1

    def _line_changed(self, no: int):
        if self._current_type != "" and self._first_extrude_line == -1:
            self._first_extrude_line = no

        self._last_extrude_line = no

    def _tool_changed(self, context: Context, new_tool: int):
        if self._current_tool != new_tool:
            self.add_section(context)
            self._current_tool = new_tool

            tool = Tool(self._current_tool)
            if tool is not None:
                context[PrintInfo].used_tools.add(tool)

    def _z_changed(self, context: Context, new_z: float):
        if self._current_z != new_z:
            self.add_section(context)
            self._current_z = new_z

    def _type_changed(self, context: Context, new_type: str):
        if new_type == 'Custom':
            return

        if self._current_type != new_type:
            self.add_section(context)
            self._current_type = new_type

    def add_section(self, context: Context):
        if self._current_type in ('', 'Custom'):
            return
        if self._first_extrude_line == -1:
            return
        if self._last_extrude_line == -1:
            return

        context[PrintSections].append(
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

    def collect(self, context: Context, line: Line):
        self._collect(context, line)
        line.meta[Tool] = Tool(self._current_tool)
        line.meta[Type] = Type(self._current_type)
        line.meta[Z] = Z(self._current_z)

    def _collect(self, context: Context, line: Line):
        self._line_changed(line.no)

        if line.command == self.config.macro.print_start:
            if 'INITIAL_TOOL' in line.params:
                self._current_tool = line.params.INITIAL_TOOL
            return

        toolchange = match.toolchange(line)
        if toolchange is not None:
            self._tool_changed(context, toolchange)
            return

        if not line.comment:
            return

        if line.comment.startswith("TYPE:"):
            self._type_changed(context, line.comment[5:].rstrip())
            return

        if line.comment.startswith("Z:"):
            height = parse_parameter(line.comment[2:].rstrip())
            if not isinstance(height, (int, float)):
                raise ValueError(f'Invalid height comment "{line.comment}"')

            self._z_changed(context, height)
            return
