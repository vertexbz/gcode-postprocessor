from __future__ import annotations
from typing import TYPE_CHECKING
import re

if TYPE_CHECKING:
    from gcode import ParamValue


def validate_gcode_command(cmd: str):
    if not re.match(r'^(:?[MG][0-9]+(:?\.[0-9]+)?)|(:?[A-Z_][A-Z0-9_]+)$', cmd, flags=re.IGNORECASE):
        raise ValueError(f'"{cmd}" is not a valid G-Code command')


def parse_parameter(p: str) -> ParamValue:
    match = re.match(r'^([-+]?)(\d*\.?\d+)$', p)
    if match:
        sign = match.group(1)
        value = match.group(2)

        if value.startswith('.'):
            value = '0' + value

        cls = int
        if '.' in value:
            cls = float

        number = cls(value)
        if sign == '-':
            number *= -1

        return number

    return p
