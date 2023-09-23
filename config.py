from __future__ import annotations


class Features:
    _list: list[str] = []

    def _normalize(self, feature: str):
        return feature.replace('-', '_')

    def add_once(self, feature: str):
        if not self.has(feature):
            self.add(feature)

    def has(self, feature: str):
        return self._normalize(feature) in self._list

    def read(self) -> list[str]:
        return self._list[:]

    def add(self, feature: str):
        self._list.append(self._normalize(feature))

    def is_empty(self) -> bool:
        return len(self._list) == 0



class Config:
    feature = Features()
    dry_run = False
