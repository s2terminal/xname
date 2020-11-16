from itertools import permutations
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

def search_xname(original_name: str):
    original_name = (original_name + 'x').lower()
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
    return (max_name.title(), max_score)

if __name__ == '__main__':
    original_name = input('input name: ')
    max_names, score = search_xname(original_name)
    print("{}は{}になりました。スコア: {}".format(original_name, max_names, score))
