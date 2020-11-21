from itertools import permutations

from src.common import name_score

def search_xname(original_name: str):
    max_score = 0
    max_name = original_name
    for v in permutations([ n for n in original_name ]):
        name = "".join(v)
        score = name_score(name, original_name)
        # if (max_score == score):
        #     max_names.append(name)
        if (max_score < score):
            max_score = score
            max_name = name
    return (max_name, max_score)
