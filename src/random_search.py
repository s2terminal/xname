import random
from typing import Callable, List
import math

from src.common import name_score

DEFAULT_SEARCH_TIMES = 100

def random_search_base(name: str, name_generator: Callable[[str], str], times: int):
    original_name = name
    best_score = -float('inf')
    best_name = name
    for _ in range(0, times):
        tmp_name = name_generator(name)

        score = name_score(tmp_name, original_name)
        if (best_score < score):
            best_score = score
            best_name = tmp_name
    return best_name, best_score

def search_ary(name: str, times=DEFAULT_SEARCH_TIMES):
    def name_generator(name: str):
        size = len(name)
        x = [random.randint(0, size - 1) + i/size for i in range(0, size)]
        name_list = list(zip([a for a in name], x))
        return "".join([x[0] for x in sorted(name_list, key=lambda x: x[1])])

    return random_search_base(name, name_generator, times)

def search_map(name: str, times=DEFAULT_SEARCH_TIMES):
    def func(ary: List, i: int) -> List:
        n = len(ary)
        if n <= 1:
            return ary
        val = ary.pop(i % n)
        ret = func(ary, i // n)
        ret.extend([val])
        return ret

    name_generator = lambda name: "".join(
        func([a for a in name], random.randint(0, math.factorial(len(name)) - 1))
    )

    return random_search_base(name, name_generator, times)
