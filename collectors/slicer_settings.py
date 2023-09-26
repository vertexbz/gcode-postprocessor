from __future__ import annotations
from typing import TYPE_CHECKING, Union, Iterable
from base import Collector
import re
from gcode import parse_parameter

if TYPE_CHECKING:
    from base import Context
    from gcode import Line, ParamValue


def parse_config_parameter(
    key: str, value: str
) -> Union[ParamValue, list[Union[int, float]], list[str], list[tuple[Union[int, float], Union[int, float]]]]:
    value = value.strip()
    # check coordinates param
    if re.match(r'^[-+]?\d*\.?\d+[xX][-+]?\d*\.?\d+(:?\s*[,;]\s*[-+]?\d*\.?\d+[xX][-+]?\d*\.?\d+)+$', value):
        values = re.split(r'[,;]', value)
        values = map(lambda v: re.split(r'[xX]', v), values)
        values = map(lambda c: (parse_parameter(c[0]), parse_parameter(c[1])), values)
        return list(values)

    if re.match(r'^[-+]?\d*\.?\d+%?(:?\s*[,;]\s*[-+]?\d*\.?\d+%?)+$', value):
        values = re.split(r'[,;]', value)
        values = map(lambda v: parse_parameter(v), values)
        return list(values)

    if not key.endswith('_gcode') and not key.startswith('gcode_') and '"' not in value and (';' in value or ',' in value):
        values = re.split(r'[,;]', value)
        values = map(lambda v: parse_parameter(v), values)
        return list(values)

    if value.startswith('"') and value.endswith('"') and '";"' in value:
        values = re.split(r'(?<!\\)";"', value[1:-1])
        return list(values)

    if key in ('post_process',):
        return value[1:-1]

    return parse_parameter(value)


class guard:
    pass


class SlicerSettings:
    def __init__(self):
        self._data = {}

    def get(self, key: str, default=guard):
        if default != guard and key.lower() not in object.__getattribute__(self, '_data'):
            return default
        return object.__getattribute__(self, '_data')[key.lower()]

    def set(self, key: str, value):
        object.__getattribute__(self, '_data').update({key.lower(): value})

    def __len__(self):
        return len(object.__getattribute__(self, '_data'))

    def __contains__(self, key: str):
        return key.lower() in object.__getattribute__(self, '_data')

    def __getitem__(self, key: str):
        return object.__getattribute__(self, '_data')[key.lower()]

    def __getattr__(self, key: str):
        return object.__getattribute__(self, '_data')[key.lower()]

    def __repr__(self):
        return object.__getattribute__(self, '_data').__repr__()

    def __str__(self):
        return object.__getattribute__(self, '_data').__str__()


class CollectSlicerSettings(Collector):
    finished = False
    began = False

    def collect(self, context: Context, line: Line):
        if not line.is_comment:
            return

        if line.comment in ('SuperSlicer_config = end', 'prusaslicer_config = begin'):
            self.finished = True
            return

        if line.comment in ('SuperSlicer_config = begin', 'prusaslicer_config = end'):
            self.began = True
            return

        if not self.began:
            return

        setting = line.comment.split(' = ', 1)
        key = setting[0]
        value = setting[1] if len(setting) == 2 else ''
        context[SlicerSettings].set(key, parse_config_parameter(key, value))
