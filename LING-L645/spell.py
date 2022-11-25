import re
from collections import Counter


def words(text):
    return re.findall(r'\w-?\w+', text.lower())

#def fourgrams(text):
#    return re.findall(r"\w{4}", text.lower())

WORDS = Counter(words(open('wiki.txt').read()))

#FOUR = Counter(fourgrams(open('wiki.txt').read()))

def P(word, N=sum(WORDS.values())):
    "Probability of 'word'."
    return WORDS[word] / N

#def PF(fourgram, N=sum(FOUR.values())):
#    "Probability of 'fourgram'"
#    return FOUR[fourgram] / N

def correction(word):
    "Most probable spelling correction for word."
    return max(candidates(word), key=P)

#def correction_F(fourgram):
#    "Most probable spelling correction for n-gram"
#    return max

def candidates(word):
    "Generate possible spelling corrections for word."
#    if word in (known([word]) or known(edits1(word)) or known(edits2(word))):
#        return (known([word]) or known(edits1(word)) or known(edits2(word))) 
#    else:
#        return try_fourgrams(word)
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

#def try_fourgrams(word):
#    return (known_grams(edits1(word)))

def known(words):
    "The subset of 'words' that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)

#def known_grams(fourgrams):
#    "The subset of 'fourgrams' that appear in the dictionary of FOUR."
#    return set(f for f in fourgrams if f in FOUR)

def edits1(word):
    "All edits that are one edit away from 'word'"
    letters = 'abcdefghijklmnopqrstuvwxyz'
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [L + R[1:] for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces = [L + C + R[1:] for L, R in splits if R for C in letters]
    inserts = [L + C + R for L, R in splits for C in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word):
    "All edits that are two edits away from 'word'."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))
