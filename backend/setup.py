# build pre-trained model
from gensim.models import Word2Vec
import numpy as np

with open('assets/codenames_words.txt', 'r') as f:
    codenames_words = f.read().strip()
with open('assets/princeton_words.txt', 'r') as f:
    princeton_words = f.read().strip()
codenames_words = codenames_words.split('\n')
princeton_words = princeton_words.upper().split('\n')

model = Word2Vec.load('assets/codenames.model')

print(model.wv.most_similar('fine_hall'))

freqs = np.loadtxt('assets/unigram_freq.csv', delimiter=',', dtype=[('word', 'U30'), ('count', 'i8')], skiprows=1)
freq_dict = {word: count for word, count in freqs}

for word in princeton_words:
    word = word.lower().replace(' ', '_')
    freq_dict.update({word: 23135851162})


# 1. Get current vocabulary
old_vocab = model.wv.key_to_index
old_vectors = model.wv.vectors

# 1.a extend frequencies to princeton words not in freq_dict
fallback_freq = 23135851161
extended_freq = {
    word: freq_dict.get(word, fallback_freq)  # if not in freq_dict, give default high frequency
    for word in old_vocab.keys()
}

# 2. Create your new vocab order
sorted_vocab = sorted(old_vocab.keys(), key=lambda w: extended_freq[w], reverse=True)

# 3. Filter to words that actually exist in the model
# sorted_vocab = [w for w in sorted_vocab if w in old_vocab]

# 4. Rebuild vectors in the new order
# new_vectors = np.array([model.wv[w] for w in sorted_vocab])
new_vectors = np.array([model.wv[word] for word in sorted_vocab])

# 5. Update the model's internal structures
# model.wv.key_to_index = {word: i for i, word in enumerate(sorted_vocab)}
# model.wv.index_to_key = sorted_vocab
# model.wv.vectors = new_vectors
model.wv.key_to_index = {word: i for i, word in enumerate(sorted_vocab)}
model.wv.index_to_key = sorted_vocab
model.wv.vectors = new_vectors
model.wv.fill_norms(force=True)

print(model.wv.most_similar('fine_hall', restrict_vocab=2000))