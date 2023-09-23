from __future__ import annotations
from typing import Optional
import re
from base import Number
import const as CONST


def match_xy_move(line: str):
    match = re.search(rf'^G[01]\sX({CONST.REGEX.FIND_NUMBER})\sY({CONST.REGEX.FIND_NUMBER})', line,
                      flags=re.IGNORECASE)
    if match:
        return (Number(match.group(1)), Number(match.group(2)))

    return None


def match_z_move(line: str):
    match = re.search(rf'^G[01]\sZ({CONST.REGEX.FIND_NUMBER})', line, flags=re.IGNORECASE)
    if match:
        return Number(match.group(1))

    return None


def match_z_only_move(line: str):
    match = match_z_move(line)
    if match is None:
        return None

    if re.search(rf'\sX({CONST.REGEX.FIND_NUMBER})', line, flags=re.IGNORECASE) \
        or re.search(rf'\sY({CONST.REGEX.FIND_NUMBER})', line, flags=re.IGNORECASE) \
        or re.search(rf'\sE({CONST.REGEX.FIND_NUMBER})', line, flags=re.IGNORECASE):
        return None

    return match


def match_extruder_move(line: str) -> Optional[Number]:
    if not line.startswith('G1 ') and not line.startswith('G0 '):
        return None

    match = re.search(rf'\sE({CONST.REGEX.FIND_NUMBER})', line, flags=re.IGNORECASE)
    if match:
        return Number(match.group(1))

    return None


def match_retraction(line: str):
    match = match_extruder_move(line)
    if match is None:
        return None

    if not match.raw.startswith('-'):
        return None

    if re.search(rf'\sX({CONST.REGEX.FIND_NUMBER})', line, flags=re.IGNORECASE) \
        or re.search(rf'\sY({CONST.REGEX.FIND_NUMBER})', line, flags=re.IGNORECASE):
        return None

    return match
