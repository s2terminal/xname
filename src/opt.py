import random
import Levenshtein
import typing
import math

vowels = [ a for a in "aiueo" ]
def name_score(name: str, original: str) -> int:
    score = 0
    is_vowel = None
    for s in name:
        if (is_vowel is not None and (is_vowel or (s in vowels))): score += 1
        is_vowel = (s in vowels)
    score /= (len(name) - 1)
    score -= (1 - (Levenshtein.distance(name, original)) / (len(name)))
    return score

def random_search(name: str, times=10):
    size = len(name)
    best_score = -float('inf')
    best_name = name
    for _ in range(0, times):
        x = []
        for i in range(0, size):
            x.append(random.randint(0, size - 1) + i/size)

        name_ary = [a for a in name]
        name_dict = dict(zip(name_ary, x))

        tmp_name = "".join(dict(sorted(name_dict.items(), key=lambda x: x[1])).keys())

        score = name_score(tmp_name, original_name)
        if (best_score < score):
            best_score = score
            best_name = tmp_name
    return best_name, best_score

def func(ary: typing.List, i: int) -> typing.List:
    n = len(ary)
    if n <= 1:
        return ary
    val = ary.pop(i % n)
    ret = func(ary, i // n)
    ret.extend([val])
    return ret

def random_search_map(name: str, times=10):
    original_name = name
    size = len(name)
    best_score = -float('inf')
    best_name = name
    for _ in range(0, times):
        x = random.randint(0, math.factorial(size) - 1)
        name_ary = [a for a in name]
        tmp_name = "".join(func(name_ary, x))

        score = name_score(tmp_name, original_name)
        if (best_score < score):
            best_score = score
            best_name = tmp_name
    return best_name, best_score
