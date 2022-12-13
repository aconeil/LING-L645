import sys, math, re, pickle
from collections import defaultdict, Counter

def tokenise(s):
    """Tokenise a line"""
    o = re.sub('([^a-zA-Z0-9\']+)', ' \g<1>', s.strip())
    s = re.sub('  *', ' ', o).split(' ')
    return s

model = defaultdict(lambda : defaultdict(float))

bigrams, unigrams = defaultdict(Counter), Counter() # Unigram and bigram counts

line = sys.stdin.readline()
length = 0
while line: # Collect counts from standard input
    tokens = ['<BOS>'] + tokenise(line)
    print(tokens)
    length += len(tokens)
    for i in range(len(tokens) - 1):
        bigrams[tokens[i]][tokens[i+1]] += 1
        unigrams[tokens[i]] += 1
    line = sys.stdin.readline()
print(bigrams)
for i in bigrams: # Calculate probabilities
    #for word j that exists in the bigram
    for j in bigrams[i]:
        #model[i][j] gives the probability of the bigram as normalized by the frequency of the first unigram in each bigram
        model[i][j] = (bigrams[i][j] / unigrams[i])
    #below statement overwrites [i][j] if used
        model["unigrams"][i]= (unigrams[i] / length)

print('Saved %d bigrams.' % sum([len(i) for i in model.items()]))
pickle.dump(dict(model), open('model.lm', 'wb'))
#print(dict(model))

#for key in (dict(model)):
#	print(dict(model[key]))
