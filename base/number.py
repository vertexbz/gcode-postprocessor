from __future__ import annotations


class Number: # todo remove
    def __init__(self, raw: str) -> None:
        self.raw = raw
        # todo correct int/float and missing zero
        self.value = float(raw)

    def __str__(self):
        return self.raw

    def __repr__(self):
        return self.raw
