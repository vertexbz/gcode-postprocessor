from __future__ import annotations
from typing import Type, TypeVar, Union

T = TypeVar('T')
I = TypeVar('I')


class guard:
    pass


class Meta:
    _data: dict[Type[T], T]
    _frozen: bool

    def __init__(self):
        self._data = {}
        self._frozen = False

    def freeze(self):
        self._frozen = True

    def get(self, key: Type[I], default: Union[None, I, guard]) -> Union[None, I]:
        if key not in self._data:
            if not self._frozen:
                self._data[key] = key()
            else:
                if default != guard:
                    return default
                raise KeyError(f'no metadata for key {type(key).__name__}')

        return self._data[key]

    def __getitem__(self, key: Type[I]) -> I:
        if key not in self._data:
            if not self._frozen:
                self._data[key] = key()
            else:
                raise KeyError(f'no metadata for key {type(key).__name__}')

        return self._data[key]

    def __setitem__(self, key: Type[I], value: I):
        if self._frozen:
            raise KeyError(f'cannot change value of key {type(key).__name__} when frozen')
        self._data[key] = value