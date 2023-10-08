from __future__ import annotations
from typing import TYPE_CHECKING, Optional, Union
import re

if TYPE_CHECKING:
    from gcode.line import Line

ParamValue = Union[int, float, str]


class guard:
    pass


class ParamsHelper:
    def __init__(self, line: Line):
        object.__setattr__(self, '_line', line)

    def items(self):
        line: Line = object.__getattribute__(self, '_line')
        return line._params.items()

    def keys(self):
        line: Line = object.__getattribute__(self, '_line')
        return line._params.keys()

    def values(self):
        line: Line = object.__getattribute__(self, '_line')
        return line._params.values()

    def __len__(self):
        line: Line = object.__getattribute__(self, '_line')
        return len(line._params)

    def __contains__(self, key: str):
        line: Line = object.__getattribute__(self, '_line')
        return key in line._params

    def get(self, key: str, default=guard):
        line: Line = object.__getattribute__(self, '_line')
        if default != guard and key not in line._params:
            return default
        return line._params[key]

    def __getitem__(self, key: str):
        line: Line = object.__getattribute__(self, '_line')
        return line._params[key]

    def __getattr__(self, key: str):
        line: Line = object.__getattribute__(self, '_line')
        return line._params[key]

    def delete(self, key: str):
        line: Line = object.__getattribute__(self, '_line')
        line.set_parameter(key, None)

    def __delattr__(self, key: str):
        line: Line = object.__getattribute__(self, '_line')
        line.set_parameter(key, None)

    def __delitem__(self, key: str):
        line: Line = object.__getattribute__(self, '_line')
        line.set_parameter(key, None)

    def set(self, key: str, value: Optional[ParamValue]):
        line: Line = object.__getattribute__(self, '_line')
        line.set_parameter(key, value)

    def __setattr__(self, key: str, value: Optional[ParamValue]):
        line: Line = object.__getattribute__(self, '_line')
        line.set_parameter(key, value)

    def __setitem__(self, key: str, value: Optional[ParamValue]):
        line: Line = object.__getattribute__(self, '_line')
        line.set_parameter(key, value)

    def update(self, E=None, **F):
        if E:
            for key, val in E.items():
                self[key] = val

        for key, val in F.items():
            self[key] = val

    def __repr__(self):
        line: Line = object.__getattribute__(self, '_line')
        return line._params.__repr__()

    def __str__(self):
        line: Line = object.__getattribute__(self, '_line')
        return line._params.__str__()