from typing import Tuple, Callable, Iterator

from src.common import name_score

def local_search_base(original_name: str, neighbor_generator: Callable[[int], Iterator[int]], times=None):
    if times is None: times = len(original_name)
    best_score = -float('inf')
    best_name = ''.join(list(reversed(original_name)))
    for _ in range(times):
        (tmp_name, tmp_score) = swap_two_base(best_name, neighbor_generator)
        if (best_score < tmp_score):
            best_score = tmp_score
            best_name = tmp_name
            # print('best!', tmp_name, tmp_score)
        else:
            break
    return (best_name, best_score)

def swap_two_base(original_name: str, neighbor_generator: Callable[[int], Iterator[int]]):
    best_score = -float('inf')
    best_name = original_name
    for (i, j) in neighbor_generator(original_name):
        tmp_name = swap_name(original_name, [i,j])
        tmp_score = name_score(tmp_name, original_name)
        # print(tmp_name, tmp_score)
        if (best_score < tmp_score):
            best_score = tmp_score
            best_name = tmp_name
    return (best_name, best_score)

def swap_two_any_neighbor(name: str) -> Iterator[int]:
    size = len(name)
    for i in range(0, size - 1):
        for j in range(i + 1, size):
            yield (i, j)

def swap_two_adjacent_neighbor(name: str) -> Iterator[int]:
    size = len(name)
    for i in range(0, size - 1):
        yield (i, i + 1)

def swap_name(name: str, swaps: Tuple[int, int]) -> str:
    name_ary = [a for a in name]
    ret = ""
    for i in range(len(name)):
        key = i
        if   i == swaps[0]: key = swaps[1]
        elif i == swaps[1]: key = swaps[0]
        ret += name_ary[key]
    return ret

def search_swap_two_any(name):      return local_search_base(name, swap_two_any_neighbor)
def search_swap_two_adjacent(name): return local_search_base(name, swap_two_adjacent_neighbor)
