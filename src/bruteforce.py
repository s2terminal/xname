from itertools import permutations

from src.common import name_score

def search_xname(original_name: str):
    best_score = 0
    best_name = original_name
    for v in permutations([ n for n in original_name ]):
        name = "".join(v)
        score = name_score(name, original_name)
        # if (max_score == score):
        #     max_names.append(name)
        if (best_score < score):
            best_score = score
            best_name = name
    return (best_name, best_score)
