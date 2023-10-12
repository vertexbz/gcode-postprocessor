from __future__ import annotations
from typing import TYPE_CHECKING, Optional
import re

if TYPE_CHECKING:
    from gcode.line import Line


def move(line: Line, X: Optional[bool] = None, Y: Optional[bool] = None, Z: Optional[bool] = None, E: Optional[bool] = None) -> bool:
    if line.command not in ('G0', 'G1'):
        return False

    if X and 'X' not in line.params:
        return False

    if Y and 'Y' not in line.params:
        return False

    if Z and 'Z' not in line.params:
        return False

    if E and 'E' not in line.params:
        return False

    if X is False and 'X' in line.params:
        return False

    if Y is False and 'Y' in line.params:
        return False

    if Z is False and 'Z' in line.params:
        return False

    if E is False and 'E' in line.params:
        return False

    return True


def toolchange(line: Line) -> Optional[int]:
    if line.command is None:
        return None

    if re.match(r'^T[0-9]+$', line.command, flags=re.IGNORECASE) is not None:
        return int(line.command[1:])

    return None


def nozzle_temperature_change(line: Line, wait: Optional[bool] = None) -> Optional[float]:
    if line.command == 'M104' and wait is not True:
        return float(line.params.S)

    if line.command == 'M109' and wait is True:
        return float(line.params.S)

    return None


def fan_speed_change(line: Line) -> Optional[float]:
    if line.command == 'M106':
        return float(line.params.S)

    if line.command == 'M107':
        return 0.0

    return None
