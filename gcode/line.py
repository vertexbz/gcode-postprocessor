from __future__ import annotations
from typing import Optional
import re
from gcode.params import ParamsHelper, ParamValue
from gcode.utils import parse_parameter
from gcode.utils import validate_gcode_command


class Line:
    _raw = None
    _command: Optional[str] = None
    _comment: Optional[str] = None
    _initial_params: dict[str, ParamValue]
    _custom_params: dict[str, Optional[ParamValue]]

    @property
    def is_classic_command(self) -> bool:
        if not self._command:
            return False
        return re.match(r'^[MG][0-9]+(:?\.[0-9]+)?$', self._command) is not None

    @property
    def params(self):
        if not self._command:
            return {}
        return ParamsHelper(self)

    @property
    def command(self) -> Optional[str]:
        return self._command

    @command.setter
    def command(self, cmd: Optional[str]):
        if cmd == self._command:
            return
        if cmd is None:
            self._raw = re.sub(rf'^{self._command}[^;]*', '', self._raw.lstrip(), flags=re.IGNORECASE)
        else:
            validate_gcode_command(cmd)
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
                self._raw = self._raw.rstrip('\n') + ' ' + glue + cmt + '\n'
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
        self._raw = line
        self._initial_params = {}
        self._custom_params = {}
        self._command = None
        self._comment = None

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
                        self._initial_params[param_str[0].upper()] = parse_parameter(param_str[1:])
                    else:
                        p = param_str.split('=', 1)
                        self._initial_params[p[0].upper()] = parse_parameter(p[1])

    def __init__(self, line: str, no: Optional[int] = None):
        self.no = no
        self.raw = line

    def __repr__(self):
        return self._raw.rstrip()

    def __str__(self):
        return self._raw.rstrip()

    def clear(self):
        self._raw = ''
        self._initial_params = {}
        self._custom_params = {}
        self._command = None
        self._comment = None

    @property
    def is_comment(self) -> bool:
        return self._command is None and self._comment is not None

    @property
    def is_empty(self) -> bool:
        return self._command is None and self._comment is None
