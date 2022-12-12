
from math import log
import numpy as np
import json
import seaborn as sn
import matplotlib.pyplot as plt

# beam search
def beam_search_decoder(data, k):
	sequences = [[list(), 0.0]]
	# walk over each step in a sequence
	#define shape as utterances versus letters
	max_T, max_A = data.shape

	# Loop over time
	for t in range(max_T):
		all_candidates = list()
		#expand each current candidate
		for i in range(len(sequences)):
			seq, score = sequences[i]
			# Loop over possible alphabet outputs
			for c in range(max_A - 1):
				candidate = [seq + [c], score - log(data[t, c])]
				#data[t, c] is the likelihood of a letter per data point at time t
				#print(t, c, data[t, c])
				all_candidates.append(candidate)
		# order all candidates by score
		ordered = sorted(all_candidates, key=lambda tup:tup[1])
		#select k best
		sequences = ordered[:k]
	return sequences

with open("output.json", "r") as read_file:
	data = json.load(read_file)
	alphabet = data["alphabet"]
	data = data["logits"]

#data = [[0.1, 0.2, 0.3, 0.4, 0.5],
#        [0.4, 0.3, 0.5, 0.2, 0.1],
#        [0.1, 0.2, 0.3, 0.4, 0.5],
#        [0.5, 0.4, 0.3, 0.2, 0.1],
#        [0.1, 0.2, 0.3, 0.4, 0.5],
#        [0.5, 0.4, 0.3, 0.2, 0.1],
#        [0.1, 0.2, 0.3, 0.4, 0.5],
#        [0.5, 0.4, 0.3, 0.2, 0.1],
#        [0.1, 0.2, 0.3, 0.4, 0.5],
#        [0.3, 0.4, 0.5, 0.2, 0.1]]

data = np.array(data)

beam_width = 3

# decode sequence using
result = beam_search_decoder(data, beam_width)
# print result
for i, seq in enumerate(result):
	if int(i) == (beam_width - 1):
		previous_element = 0
		for element in seq[0]:
			if element == previous_element:
				continue
			else:
				previous_element = element
				print(alphabet[element], end=" ")

#make a heatmap showing the likelihood of each character
sn.heatmap(data.transpose(), cmap=sn.cm.rocket_r, yticklabels = alphabet)
plt.savefig('example.png')