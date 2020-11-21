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
