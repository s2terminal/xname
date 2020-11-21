from typing import Callable, Tuple

from src import bruteforce
from src import random_search
from src import pulp_search

def xname(name: str, method: Callable[[str], Tuple[str, float]], en_x: bool = True):
    name = name.lower()
    if en_x:
        name += "x"
    else:
        name = name.replace("x", "", 1)
    xnames = method(name)
    return (xnames[0].title(), xnames[1], method)

if __name__ == '__main__':
    original_name = input('input name: ')

    print(xname(original_name, pulp_search.solver))
    print(xname(original_name, random_search.search_ary))
    print(xname(original_name, random_search.search_map))
    print(xname(original_name, bruteforce.search_xname))
