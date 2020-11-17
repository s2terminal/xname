import random
import Levenshtein

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
    name += "x"
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

if __name__ == '__main__':
    original_name = input('input name: ')
    xname = random_search(original_name)
    print(xname)
