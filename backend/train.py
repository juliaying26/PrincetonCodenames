import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
import re
from gensim import downloader
from gensim.models import Word2Vec
from gensim import downloader
from collections import Counter

nltk.download('punkt_tab')

# tokenize training corpus

# read file
with open('assets/princeton_train_corpus.txt', 'r', encoding='utf-8') as f:
  text = f.read()

# convert to lowercase
text = text.lower()

# find synonyms
synonyms = [['residential college', 'res college', 'resco'], ['tiger inn', 'ti'], ['cap and gown', 'cap', 'cap & gown'], ['colonial', 'colo'], ['quad', 'quadrangle'], ['rocky', 'rockefeller'], ['ncw', 'new college west'], ['equad', 'e-quad'], ['psafe', 'public safety'], ['oa', 'outdoor action'], ['u-store', 'ustore', 'u store'], ['prox', 'tigercard'], ['lca', 'lewis center for the arts']]
for synlist in synonyms:
  for item in synlist:
    text = re.sub(rf"\b{re.escape(item)}\b", synlist[0], text)

# convert multi word phrases into a single token
multiwords = ['late meal', 'orange bubble', 'honor code', 'residential college', 'lake carnegie', 'eating club', 'tiger inn', 'cap and gown', 'campus club', 'old nassau', 'east pyne', 'cannon green', 'friend center', 'princeton junction', 'poe field', 'bent spoon', 'small world', 'fine hall', 'coffee club', 'triangle club', 'daily princetonian', 'room draw', 'nj transit']
for item in multiwords:
  new_item = item.replace(' ', '_')
  text = re.sub(item, new_item, text)

# break into sentences and tokenize
sentences = sent_tokenize(text)
tokenized_sentences = [word_tokenize(sent) for sent in sentences]

glove300 = downloader.load('glove-wiki-gigaword-300')

with open("assets/codenames_words.txt", 'r') as f:
  codenames_words = f.read()

codenames_words = codenames_words.split('\n')[1:]
codenames_words = [word.lower().split(' ') for word in codenames_words]

codenames_words = codenames_words * 8
print(codenames_words)

model = Word2Vec(vector_size=300, min_count=8)
model.build_vocab(tokenized_sentences + codenames_words)

# Copy overlapping vocab from GloVe into your model
for word in model.wv.key_to_index:
    if word in glove300:
        model.wv[word] = glove300[word]
        model.wv.set_vecattr(word, "lockf", 1.0)  # allow fine-tuning

model.train(tokenized_sentences, total_examples=len(tokenized_sentences), epochs=5)


# ## print word counts etc.
# words and stuff
# model = Word2Vec.load('assets/codenames.model')
word_counts = Counter(text.split())

# load new model
lines = []
with open('assets/princeton_words.txt') as f:
  princeton_words = f.read()

  princeton_words = princeton_words.upper().split('\n')[1:]
  for word in princeton_words:
    word = word.lower()
    if ' ' in word:
      word = word.replace(' ', '_')
    lines.append(word + " " + str(word_counts[word]))
    similar = model.wv.most_similar(word)
    lines.append(" ".join(str(item) for item in similar))

with open("assets/princeton_word_counts.txt", 'w') as f:
  for line in lines:
    f.write(line + "\n")