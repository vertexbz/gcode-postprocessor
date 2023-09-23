from __future__ import annotations


class Number:
    def __init__(self, raw: str) -> None:
        self.raw = raw
        self.value = float(raw)
