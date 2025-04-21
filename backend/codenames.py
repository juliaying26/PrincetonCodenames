from ctypes import sizeof
from gensim.models import Word2Vec
import random

model = Word2Vec.load('assets/codenames.model')

# read in files
with open('assets/codenames_words.txt', 'r') as f:
  codenames_words = f.read().strip()
with open('assets/princeton_words.txt', 'r') as f:
  princeton_words = f.read().strip()
codenames_words = codenames_words.split('\n')
princeton_words = princeton_words.upper().split('\n')

# class containing the board: the full board (with private access to which words are for which team)
class CodenamesBoard:

  # initialize board randomly
  def __init__(self, threshold):
    self._threshold = threshold
    self.game_over = False

    # choose 25 words: 5 Princeton and 20 standard Codenames clues
    chosen_words = random.sample(codenames_words, 20) + random.sample(princeton_words, 5)

    # convert to word2vec format
    for i in range(len(chosen_words)):
      chosen_words[i] = chosen_words[i].lower().replace(' ', '_')

    # shuffle to choose assassin, teams, etc
    random.shuffle(chosen_words)
    self._assassin = chosen_words[0:1] # worst word (ends game in a loss)
    self._team = chosen_words[1:10] # all 9 remaining words for this team
    self._opponents = chosen_words[10:18] # all 8 remaining words for opponent's team
    self._neutral = chosen_words[18:25] # all remaining neutral words

    self._team_copy = self._team.copy()
    self._opponents_copy = self._opponents.copy()
    self._neutral_copy = self._neutral.copy()

    # shuffle again so that the player cannot figure out which cards are which
    random.shuffle(chosen_words)
    # self._full_board = chosen_words # all cards in game

    # convert back to uppercase (format seen by player)
    for i in range(len(chosen_words)):
      chosen_words[i] = chosen_words[i].upper().replace('_', ' ')
    self._remaining_board = chosen_words # all remaining cards in game
    self._board_copy = self._remaining_board.copy()


  # get color of codenames word
  def get_color(self, word):
      print(self._remaining_board)
      if word in self._remaining_board: return '#F4EBD1'
      word = word.lower().replace(' ', '_')
      if word in self._assassin: return '#272727'
      elif word in self._team_copy: return '#40729B'
      elif word in self._opponents_copy: return '#C93B1E'
      elif word in self._neutral_copy: return '#CDC0AD'

  def get_board(self):
      grid = [self._board_copy[i:i+5] for i in range(0, len(self._board_copy), 5)]
      colored_grid = []
      for row in grid:
        colored_row = []
        for word in row:
          color = self.get_color(word)
          colored_row.append((word, color))
        colored_grid.append(colored_row)
      return colored_grid

    # print remaining cards in 5x5 grid (and return a list of cards)
  def remaining_cards(self):
      # convert to grid format and print
      return [i for i in self._remaining_board if i != '']

  # choose which cards to create a clue for, based on a safety threshhold
  def _clue_words(self, my_team=True):
      # loop through all words to find an initial pair
      highest_sim = -1
      highest_sim_word1 = None
      highest_sim_word2 = None

      if my_team: possibilities = self._team
      else: possibilities = self._opponents

      for teamword1 in possibilities:
          for teamword2 in possibilities:
              if teamword1 == teamword2: continue #skip if words are equal
              # print(teamword1, teamword2, teamword1==teamword2)
              curr_sim = model.wv.similarity(teamword1,teamword2)

              # if pair has highest similarity, save them (unless words are identical)
              if (curr_sim >= highest_sim) and (curr_sim != 1):
                  highest_sim = curr_sim
                  highest_sim_word1 = teamword1
                  highest_sim_word2 = teamword2
      print(highest_sim, highest_sim_word1, highest_sim_word2)

      # only choose this pair if above threshold
      if highest_sim >= self._threshold:
          clue_cards = [highest_sim_word1, highest_sim_word2]
          # find similarity to other cards
          for teamword in self._team:
              # do not add multiple identical words!
              if (teamword == highest_sim_word1) or (teamword == highest_sim_word2):
                  continue

          # if both similarities are high, add the word to the clue set
          similarity1 = model.wv.similarity(highest_sim_word1, teamword)
          similarity2 = model.wv.similarity(highest_sim_word2, teamword)
          print(teamword, similarity1, similarity2)
          if (similarity1 >= self._threshold) and (similarity2 >= self._threshold):
              clue_cards.append(teamword)

      # if no pairs are above threshold, choose word least similar to everything else
      else:
        lowest_ave_sim = 100
        lowest_sim_word = None
        for teamword1 in possibilities:
          curr_ave = 0

          # compare to all other team words
          for teamword2 in possibilities:
            if teamword1 == teamword2: continue #skip if words are equal

            curr_sim = model.wv.similarity(teamword1,teamword2)
            curr_ave += curr_sim**2

          # find lowest sim
          if (curr_ave <= lowest_ave_sim):
            lowest_ave_sim = curr_ave
            lowest_sim_word = teamword1
        clue_cards = [lowest_sim_word]
        # clue_cards = [random.choice(possibilities)]

      print(clue_cards)
      return clue_cards

  # create a clue, based on the current board
  def get_clue(self):
    # choose which cards to create a clue for
    clue_cards = self._clue_words()

    # find potential negative words that are too similar to clue words
    all_neg = self._assassin + self._opponents + self._neutral
    problematic_neg = []
    for neg_word in all_neg:
      # compare to all words we want to create a clue for
      # if it is too similar to any of the clue words, it might be problematic
      for curr_clue in clue_cards:
        curr_sim = model.wv.similarity(neg_word, curr_clue)
        if curr_sim >= self._threshold:
          problematic_neg.append(neg_word)
          break

    # find clue using word2vec.most_similar()
    print(f'problematic: {problematic_neg}')
    clues = model.wv.most_similar(positive=clue_cards, negative=problematic_neg, topn=20, restrict_vocab=5000)
    print(f'clue options: {clues}')

    # choose clue with highest similarity that is alphabetic (with - or _)
    def _acceptable(clue_str):
      return all(char.isalpha() or char in "-_" for char in clue_str)
    for curr_clue, curr_freq in clues:
      if _acceptable(curr_clue):
        print(f'clue = {curr_clue}, {len(clue_cards)}')
        return curr_clue, len(clue_cards)

    return '', 0

  # respond to a user's guess (remove guessed card from lists)
  def team_guesses(self, guess):
    msg = ''
    if guess == 'no additional guesses this round':
      msg += 'No additional guesses this round.\n'
      return msg

    # remove guess from remaining board (replacing with '')
    self._remaining_board = ['' if item == guess else item for item in self._remaining_board]

    lower_guess = guess.lower().replace(' ', '_')

    # handle correct case
    if lower_guess in self._team:
      self._team.remove(lower_guess)
      # print(f'{guess} was correct!')
      msg += f'{guess} was correct!\n'
    # handle opponent case
    elif lower_guess in self._opponents:
      self._opponents.remove(lower_guess)
      # print(f'{guess} was for the opposing team!')
      msg += f'{guess} was for the opposing team!\n'
      # end round without checking other guesses
      return msg
    
    # handle neutral case
    elif lower_guess in self._neutral:
      # print(f'{guess} was a bystander!')
      msg += f'{guess} was a bystander!\n'
      self._neutral.remove(lower_guess)
      return msg
    
    # handle assassin case
    elif lower_guess in self._assassin:
      msg += f'GAME OVER (assassin found): COMPUTER WINS\n'
      # print(f'GAME OVER (assassin found): COMPUTER WINS')
      self.game_over = True
      return msg
    
    return msg

  # create a clue for the opponent
  def opponent_get_clue(self):
    # choose which cards to create a clue for
    clue_cards = self._clue_words(my_team=False)

    # find potential negative words that are too similar to clue words
    all_neg = self._assassin + self._team + self._neutral
    problematic_neg = []
    for neg_word in all_neg:
      # compare to all words we want to create a clue for
      # if it is too similar to any of the clue words, it might be problematic
      for curr_clue in clue_cards:
        curr_sim = model.wv.similarity(neg_word, curr_clue)
        if curr_sim >= self._threshold:
          problematic_neg.append(neg_word)
          break

    # find clue using word2vec.most_similar()
    print(f'problematic: {problematic_neg}')
    clues = model.wv.most_similar(positive=clue_cards, negative=problematic_neg, topn=20, restrict_vocab=5000)
    print(f'clue options: {clues}')

    # choose clue with highest similarity that is alphabetic (with - or _)
    def _acceptable(clue_str):
      return all(char.isalpha() or char in "-_" for char in clue_str)
    for curr_clue, curr_freq in clues:
      if _acceptable(curr_clue):
        print(f'clue = {curr_clue}, {len(clue_cards)}')
        return curr_clue, len(clue_cards)

    return '', 0

  # simulate opponent's round
  def opponent_guess(self, clue, clue_size):
    accuracy = 0.8

    # sort all remaining cards by similarity to clue
    possibilities = []
    for word in board._remaining_board:
      if word != '': possibilities.append(word)
    similarities = [model.wv.similarity(clue, word.lower().replace(' ', '_')) for word in possibilities]
    both = []
    for x, y in zip(possibilities, similarities):
        both.append((x, y))
    both = sorted(both, key=lambda element: element[1], reverse=True)

    msg = ''
    for i in range(clue_size):
      value = random.random()
      # with prob accuracy, select best word from our cards
      if value > accuracy: guess = both[0][0]
      # with prob 1-accuracy, select random guess
      else: guess = random.choice(possibilities)

      # remove from remaining cards
      self._remaining_board = ['' if item == guess else item for item in self._remaining_board]

      # check guess
      print(f'opponent guessed {guess}')
      lower_guess = guess.lower().replace(' ', '_')
      # handle correct case
      if lower_guess in self._team:
        self._team.remove(lower_guess)
        # print(f'{guess} was a word for YOUR team!')
        msg += f'{guess} was a word for YOUR team!\n'
        break
      # handle opponent case
      elif lower_guess in self._opponents:
        self._opponents.remove(lower_guess)
        # print(f'{guess} was correct!')
        msg += f'{guess} was correct!\n'
      # handle neutral case
      elif lower_guess in self._neutral:
        # print(f'{guess} was a bystander!')
        msg += f'{guess} was a bystander!\n'
        self._neutral.remove(lower_guess)
        break
      # handle assassin case
      elif lower_guess in self._assassin:
        # print(f'GAME OVER (assassin found): YOU WIN')
        msg += f'GAME OVER (assassin found): YOU WIN\n'
        self.game_over = True
        break
    return msg

# initialize board for this game, and view all of the cards
board = CodenamesBoard(.25)
board.get_clue()
board.opponent_get_clue()