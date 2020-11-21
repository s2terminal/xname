from typing import Callable, Tuple
import sys

from src import bruteforce
from src import random_search
from src import pulp_search
from src import local_search

def xname(name: str, method: Callable[[str], Tuple[str, float]], en_x: bool = True):
    name = name.lower()
    if en_x:
        name += "x"
    else:
        name = name.replace("x", "", 1)
    xnames = method(name)
    return (xnames[0].title(), xnames[1], method)

if __name__ == '__main__':
    args = sys.argv
    if len(args) == 2:
        original_name = args[1]
    else:
        original_name = input('input name: ')

    en_x = True

    print(xname(original_name, pulp_search.solver, en_x))
    print(xname(original_name, random_search.search_ary, en_x))
    print(xname(original_name, random_search.search_map, en_x))
    print(xname(original_name, local_search.search_swap_two_any, en_x))
    print(xname(original_name, local_search.search_swap_two_adjacent, en_x))
    print(xname(original_name, bruteforce.search_xname, en_x))
