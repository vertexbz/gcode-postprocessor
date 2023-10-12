from __future__ import annotations
from typing import Optional
from functools import cached_property
import re

from gcode.meta import Meta
from gcode.params import ParamsHelper, ParamValue
from gcode.utils import parse_parameter
from gcode.utils import validate_gcode_command


class Line:
    _raw = None
    _command: Optional[str] = None
    _comment: Optional[str] = None
    _params: dict[str, ParamValue]

    @cached_property
    def is_classic_command(self) -> bool:
        if not self._command:
            return False
        return re.match(r'^[MG][0-9]+(:?\.[0-9]+)?$', self._command) is not None

    @cached_property
    def params(self):
        if not self._command:
            return {}
        return ParamsHelper(self)

    @property
    def meta(self):
        return self._meta

    @property
    def command(self) -> Optional[str]:
        return self._command

    @command.setter
    def command(self, cmd: Optional[str]):
        if cmd == self._command:
            return

        self.__dict__.pop('is_classic_command', None)

        if cmd is None:
            self._raw = re.sub(rf'^{self._command}[^;]*', '', self._raw.lstrip(), flags=re.IGNORECASE)
        else:
            validate_gcode_command(cmd)
            # todo check params on modern<>classic conversion
            cmd = cmd.upper()
            if self._command is None:
                old_raw = self._raw
                self._raw = cmd
                if len(old_raw.strip()) > 0:
                    self._raw += ' ' + old_raw
                else:
                    self._raw += '\n'
            else:
                self._raw = re.sub(rf'^{self._command}', cmd, self._raw.lstrip(), flags=re.IGNORECASE)
        self._command = cmd

    @property
    def comment(self) -> Optional[str]:
        return self._comment

    @comment.setter
    def comment(self, cmt: Optional[str]):
        if cmt == self._comment:
            return
        if cmt is None:
            self._raw = re.sub(rf'\s*;\s*{self._comment}\s*$', '', self._raw)
        else:
            glue = '; '
            if self._comment is None:
                if self._command is not None:
                    glue = ' ' + glue
                self._raw = self._raw.rstrip('\n') + glue + cmt + '\n'
            else:
                self._raw = re.sub(rf';\s*{self._comment}', glue + cmt, self._raw)
        self._comment = cmt

    @property
    def raw(self):
        return self._raw

    @raw.setter
    def raw(self, line: str):
        if self._raw == line:
            return
        self.remove()
        self._raw = line

        stripped = line.strip()
        if len(stripped) == 0:
            return

        s = re.split(r'[\s;]', stripped, 1)
        if len(s[0]) > 0:
            validate_gcode_command(s[0])
            command = s[0].upper()
            self._command = command

        if len(s) > 1:
            rest = (stripped[len(s[0])] + s[1]).strip()
            s = rest.split(';', 1)
            if len(s) > 1:
                self._comment = s[1].strip()
            params_str = re.sub(r'\s+', ' ', s[0]).strip()
            if len(params_str) > 0:
                params_strs = params_str.split(' ')
                for param_str in params_strs:
                    if self.is_classic_command:
                        self._params[param_str[0].upper()] = parse_parameter(param_str[1:])
                    else:
                        p = param_str.split('=', 1)
                        self._params[p[0].upper()] = parse_parameter(p[1])

    def __init__(self, line: str, no: Optional[int] = None):
        self.no = no
        self.raw = line
        self._meta = Meta()

    def __repr__(self):
        return self._raw.rstrip()

    def __str__(self):
        return self._raw.rstrip()

    def clear(self):
        self.remove()
        self._raw = '\n'

    def remove(self):
        self._raw = ''
        self._params = {}
        self._command = None
        self._comment = None
        self.__dict__.pop('is_classic_command', None)
        self.__dict__.pop('params', None)

    @property
    def is_comment(self) -> bool:
        return self._command is None and self._comment is not None

    @property
    def is_empty(self) -> bool:
        return self._command is None and self._comment is None

    def set_parameter(self, key: str, value: Optional[ParamValue]):
        if len(key) == 0:
            raise KeyError('Empty parameter name is not allowed')

        key = key.upper()
        key_phrase = f'{re.escape(key)}='

        if self.is_classic_command:
            key_phrase = re.escape(key)
            if len(key) != 1:
                raise KeyError('Classic commands support only one letter parameters')
            if value is not None and not isinstance(value, (int, float)):
                raise KeyError('Classic commands support only numeric parameter values')

        if value is None:
            if key in self._params:
                self._raw = re.sub(rf'\s+{key_phrase}[^\s;]*', '', self._raw, flags=re.IGNORECASE)
                del self._params[key]
        else:
            if key in self._params:
                self._raw = re.sub(rf'(\s+{key_phrase}){re.escape(str(self._params[key]))}', rf'\g<1>{value}', self._raw, flags=re.IGNORECASE)
            else:
                if self._comment is None:
                    self._raw = re.sub(rf'(\s+)$', rf' {key_phrase}{value}\1', self._raw, flags=re.IGNORECASE)
                else:
                    self._raw = re.sub(rf'(\s*;)', rf' {key_phrase}{value}\1', self._raw,  flags=re.IGNORECASE)

            self._params[key] = value

