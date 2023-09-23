from __future__ import annotations
import random
import logging
import os
import sys
from sty import fg, ef


FORMAT_SHORT = f"{ef.dim}[%(levelname)s]{ef.rs}[%(name)s] %(message)s"
FORMAT_DEBUG = f"{ef.dim}%(asctime)s [%(levelname)s]{ef.rs}[%(name)s] %(message)s {ef.dim}(%(relativepath)s:%(lineno)d){ef.rs}"

class LogFormat:
    _format = FORMAT_SHORT

    def get(self) -> str:
        return self._format

    def setLongFormat(self, long: bool):
        if long:
            self._format = FORMAT_DEBUG
        else:
            self._format = FORMAT_SHORT

FORMAT = LogFormat()


class PackagePathFilter(logging.Filter):
    def filter(self, record):
        pathname = record.pathname
        record.relativepath = None
        abs_sys_paths = map(os.path.abspath, sys.path)
        for path in sorted(abs_sys_paths, key=len, reverse=True):  # longer paths first
            if not path.endswith(os.sep):
                path += os.sep
            if pathname.startswith(path):
                record.relativepath = os.path.relpath(pathname, path)
                break
        return True


class CustomFormatter(logging.Formatter):
    FORMATS = {
        logging.DEBUG: lambda f: f,
        logging.INFO: lambda f: f,
        logging.WARNING: lambda f: fg.yellow + f + fg.rs,
        logging.ERROR: lambda f: fg.red + f + fg.rs,
        logging.CRITICAL: lambda f: fg.li_red + f + fg.rs,
    }

    _colors = {
        'root': ''
    }

    def rand_color(self):
        while True:
            color = random.randint(0, 255)
            if color not in (9, 52, 88, 124, 160, 196) and color not in self._colors.values() and color < 231:
                return color

    def color_child(self, name):
        if name not in self._colors:
            self._colors[name] = fg(self.rand_color())

        return self._colors[name]

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        record.msg = log_fmt(record.msg)

        color = self.color_child(record.name)

        format = FORMAT.get().replace(ef.rs, ef.rs + color)
        format = format.replace(fg.rs, fg.rs + color)

        formatter = logging.Formatter(color + format + ef.rs)
        return formatter.format(record)


def stdout_handler():
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(CustomFormatter())
    handler.addFilter(PackagePathFilter())
    return handler


def file_handler(logfile: str):
    handler = logging.FileHandler(logfile)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter(FORMAT_DEBUG))
    handler.addFilter(PackagePathFilter())
    return handler



logger = logging.getLogger()
logger.setLevel(logging.ERROR)
logger.addHandler(stdout_handler())

FATAL = logging.FATAL
CRITICAL = logging.CRITICAL
ERROR = logging.ERROR
WARNING = logging.WARNING
WARN = logging.WARN
INFO = logging.INFO
DEBUG = logging.DEBUG

debug = logger.debug
info = logger.info
warn = logger.warn
warning = logger.warning
error = logger.error
critical = logger.critical
fatal = logger.fatal

getChild = logger.getChild
setLevel = logger.setLevel
setLongFormat = FORMAT.setLongFormat

def logToFile(logfile: str):
    logger.addHandler(file_handler(logfile))


__all__ = [
    'stdout_handler', 'file_handler',
    'getChild', 'setLevel', 'logToFile', 'setLongFormat',
    'fatal', 'critical', 'error', 'warning', 'warn', 'info', 'debug',
    'FATAL', 'CRITICAL', 'ERROR', 'WARNING', 'WARN', 'INFO', 'DEBUG',
]
