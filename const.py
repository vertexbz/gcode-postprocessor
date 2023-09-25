from __future__ import annotations
import os
import sys

SRCDIR = os.path.dirname(__file__)
VENVDIR = os.environ['VIRTUAL_ENV'] if 'VIRTUAL_ENV' in os.environ else os.path.dirname(os.path.dirname(sys.executable))
