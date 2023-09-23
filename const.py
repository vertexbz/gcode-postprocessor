from __future__ import annotations
import os
import sys


class REGEX:
    # Define the regular expression to find the numbers in the line
    FIND_NUMBER = r"[-+]?\d*\.?\d+"


SRCDIR = os.path.dirname(__file__)
VENVDIR = os.environ['VIRTUAL_ENV'] if 'VIRTUAL_ENV' in os.environ else os.path.dirname(os.path.dirname(sys.executable))
