import pickle, sys, re, numpy

model = pickle.load(open('model.lm', 'rb'))

def tokenise(s):
	"""Tokenise a line"""
	o = re.sub('([^a-zA-Z0-9\']+)', ' \g<1>', s.strip())
	s = re.sub('  *', ' ', o).split(' ')
	return s

line = sys.stdin.readline()

while line:
	#collect a list of tokens for each sentence
	tokens = ['<BOS>'] + tokenise(line)
	#The probability equals one?
	p = 1
	#for a number in the length of the sentence
	for i in range(len(tokens) -1):
		# multiply by the unigram value if there is not a bigram starting with the token
		if tokens[i+1] not in model[tokens[i]]:
			p = p / (model["unigrams"][tokens[i]] + len(model["unigrams"]))
		else:
			#p = p * model[tokens[i]][tokens[i+1]]
			#below is an attempt at smoothing
			p = p * (model[tokens[i]][tokens[i+1]] + 1) / (model["unigrams"][tokens[i]] + len(model["unigrams"]))
	print(numpy.log(p), p, tokens)
	line = sys.stdin.readline()

#for key in model:
#print(model[tokens[i]])