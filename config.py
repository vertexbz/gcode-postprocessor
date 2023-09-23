from __future__ import annotations
from typing import Optional

import logger


class Features:
    _data: list[tuple[str, Optional[dict]]] = []

    def _normalize(self, feature: str):
        return feature.replace('-', '_')

    def is_empty(self) -> bool:
        return len(self._data) == 0

    def read(self) -> list[tuple[str, Optional[dict]]]:
        return self._data[:]

    def add(self, feature: str, config: Optional[dict] = None):
        self._data.append((self._normalize(feature), config))


class Macros:
    print_start = '_PRINT_START'


class Config:
    log_level = logger.ERROR
    dry_run = False
    feature = Features()
    macro = Macros()
