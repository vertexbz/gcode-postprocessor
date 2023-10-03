from __future__ import annotations
from typing import Type, TypeVar

T = TypeVar('T')
I = TypeVar('I')


class Meta:
    _data: dict[Type[T], T]
    _frozen: bool

    def __init__(self):
        self._data = {}
        self._frozen = False

    def freeze(self):
        self._frozen = True

    def __getitem__(self, key: Type[I]) -> I:
        if key not in self._data:
            self._data[key] = key()

        return self._data[key]

    def __setitem__(self, key: Type[I], value: I):
        self._data[key] = value