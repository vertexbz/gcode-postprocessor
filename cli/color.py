from __future__ import annotations
import random

_rand_8bit_pool: dict[str, list[int]] = {}


def rand_8bit_init() -> list[int]:
    pool = set(range(10, 230 + 1))
    for banned in {52, 88, 124, 160, 196}:
        pool.remove(banned)

    pool = list(pool)
    random.Random(8).shuffle(pool)
    return pool


def rand_8bit(pool: str = ''):
    if pool not in _rand_8bit_pool or len(_rand_8bit_pool[pool]) == 0:
        _rand_8bit_pool[pool] = rand_8bit_init()
    return _rand_8bit_pool[pool].pop()
