from __future__ import annotations
import logging
import sys
from logger.filter_package_path import PackagePathFilter
from logger.formatter import CustomFormatter
from logger.format import FORMAT_DEBUG
from logger.buffered import BufferingHandler


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.setFormatter(CustomFormatter(logger))
stdout_handler.addFilter(PackagePathFilter())
buffered_stdout_handler = BufferingHandler(stdout_handler)
logger.addHandler(buffered_stdout_handler)
logger.debug('Stdout logger configured')


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


def setLevel(level):
    logger.setLevel(level)
    buffered_stdout_handler.setLevel(level)


def logToFile(logfile: str):
    handler = logging.FileHandler(logfile)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter(FORMAT_DEBUG))
    handler.addFilter(PackagePathFilter())
    logger.addHandler(handler)


class SilentError(Exception):
    pass


__all__ = [
    'SilentError',
    'getChild', 'setLevel', 'logToFile',
    'fatal', 'critical', 'error', 'warning', 'warn', 'info', 'debug',
    'FATAL', 'CRITICAL', 'ERROR', 'WARNING', 'WARN', 'INFO', 'DEBUG',
]
