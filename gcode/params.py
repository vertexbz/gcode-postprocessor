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
        self._line = line
        self._is_classic_command = line.is_classic_command

    def update(self, E=None, **F):
        if E:
            for key, val in E.items():
                self[key] = val

        for key, val in F.items():
            self[key] = val

    def items(self):
        result = []
        for key, val in self._line._initial_params.items():
            if key in self._line._custom_params:
                custom = self._line._custom_params[key]
                if custom is not None:
                    result.append((key, custom))
            else:
                result.append((key, val))

        for key, val in self._line._custom_params.keys():
            if key in self._line._initial_params:
                continue
            result.append((key, val))
        return result

    def keys(self):
        result = []
        for key in self._line._initial_params.keys():
            if self._line._custom_params.get(key, 0) is None:
                continue
            result.append(key)

        for key, val in self._line._custom_params.items():
            if val is None or key in self._line._initial_params:
                continue
            result.append(key)
        return result

    def values(self):
        result = []
        for key, val in self._line._initial_params.items():
            if key in self._line._custom_params:
                custom = self._line._custom_params[key]
                if custom is not None:
                    result.append(custom)
            else:
                result.append(val)

        for key, val in self._line._custom_params.keys():
            if key in self._line._initial_params:
                continue
            result.append(val)
        return result

    def get(self, key: str, default=guard):
        if default != guard and key not in self:
            return default
        return self[key]

    def delete(self, key: str):
        del self[key]

    def set(self, key: str, val: Optional[ParamValue]):
        self[key] = val

    def __len__(self):
        return len(self.keys())

    def __contains__(self, key: str):
        if key in self._line._custom_params:
            val = self._line._custom_params[key]
            return val is not None

        return key in self._line._initial_params

    def __getitem__(self, key: str):
        if key in self._line._custom_params:
            val = self._line._custom_params[key]
            if val is None:
                raise KeyError(f'Invalid param "{key}"')
            return val

        return self._line._initial_params[key]

    def __getattr__(self, key: str):
        if key in ('_line', '_is_classic_command'):
            return object.__getattribute__(self, key)
        return self[key]

    def __delitem__(self, key: str):
        self[key] = None

    def __delattr__(self, key: str):
        self[key] = None

    def __setattr__(self, key: str, value: Optional[ParamValue]):
        if key in ('_line', '_is_classic_command'):
            object.__setattr__(self, key, value)
        else:
            self[key] = value

    def __setitem__(self, key: str, value: Optional[ParamValue]):
        if len(key) == 0:
            raise KeyError('Empty parameter name is not allowed')

        key = key.upper()
        key_phrase = f'{key}='

        if self._is_classic_command:
            key_phrase = key
            if len(key) != 1:
                raise KeyError('Classic commands support only one letter parameters')
            if value is not None and not isinstance(value, (int, float)):
                raise KeyError('Classic commands support only numeric parameter values')

        if value is None:
            if key in self:
                self._line._raw = re.sub(rf'\s+{key_phrase}[^\s;]*', '', self._line._raw, flags=re.IGNORECASE)
        else:
            if key in self:
                self._line._raw = re.sub(rf'(\s+{key_phrase}){self[key]}', rf'\g<1>{value}', self._line._raw, flags=re.IGNORECASE)
            else:
                if self._line._comment is None:
                    self._line._raw = re.sub(rf'(\s+)$', rf' {key_phrase}{value}\1', self._line._raw, flags=re.IGNORECASE)
                else:
                    self._line._raw = re.sub(rf'(\s*;)', rf' {key_phrase}{value}\1', self._line._raw,  flags=re.IGNORECASE)

        self._line._custom_params.update({key: value})
