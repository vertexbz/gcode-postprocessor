from __future__ import annotations
import logging
import sys
from logger.filter_package_path import PackagePathFilter
from logger.formatter import CustomFormatter
from logger.format import FORMAT_DEBUG


logger = logging.getLogger()

def stdout_handler():
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(CustomFormatter(logger))
    handler.addFilter(PackagePathFilter())
    return handler


def file_handler(logfile: str):
    handler = logging.FileHandler(logfile)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter(FORMAT_DEBUG))
    handler.addFilter(PackagePathFilter())
    return handler



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

def logToFile(logfile: str):
    logger.addHandler(file_handler(logfile))


__all__ = [
    'stdout_handler', 'file_handler',
    'getChild', 'setLevel', 'logToFile',
    'fatal', 'critical', 'error', 'warning', 'warn', 'info', 'debug',
    'FATAL', 'CRITICAL', 'ERROR', 'WARNING', 'WARN', 'INFO', 'DEBUG',
]
