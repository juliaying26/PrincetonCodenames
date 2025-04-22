from flask import Flask, redirect, request, jsonify, send_from_directory, abort
import codenames
import setup
import uuid

app = Flask(__name__, template_folder='../frontend', static_folder='../frontend/dist')

board = codenames.CodenamesBoard(0.25)
rounds = 2
curr_round = 0
session_id = str(uuid.uuid4())

# # Initialize persistent log display
# display(HTML("""
# <div id="game-area">
#   <div id="log" style="font-family:monospace; white-space:pre-wrap; padding:10px; background:#f9f9f9; border:1px solid #ddd; border-radius:8px; margin-bottom:20px;"></div>
#   <div id="input-area"></div>
# </div>
# """))

def game_over():
    if board.game_over:
        return True
    return False

def turn_over(guess_number, msg):
    if guess_number > board.num_guesses:
        return True
    if "opposing" in msg or "bystander" in msg:
        return True
    return False

def extra_guess(guess_number, msg):
    if not game_over() and 'assassin' not in msg and not turn_over(guess_number, msg) and board.num_guesses == guess_number:
        return True

@app.route('/api/getboard', methods=['GET'])
def get_board():
    return jsonify(board.get_board())

@app.route('/api/getdropdownoptions', methods=['GET'])
def get_dropdown_options():
    print("REMAINING", board.remaining_cards())
    return board.remaining_cards()

@app.route('/api/guessword', methods=['POST'])
def guess_word():
    global curr_round

    data = request.get_json()
    guess = data.get('word')
    guess_number = data.get('guess_number')
    
    msg = board.team_guesses(guess)
    if extra_guess(guess_number, msg):
        return jsonify({"message": msg + "\n" + "You get an extra guess!"})
    if turn_over(guess_number, msg):
        return jsonify({"message": msg + "\n" + "Your turn is over. Please wait for the other team to play."})
    
    curr_round += 1
    return jsonify({"message": msg})

@app.route('/api/opponentplay', methods=['POST'])
def opponent_play():
    clue, clue_size = board.opponent_get_clue()
    clue = clue.replace('_', ' ')
    msg = board.opponent_guess(clue, clue_size)
    print(msg)
    return jsonify({"message": msg, "clue": clue, "clue_size": clue_size})

@app.route('/api/getclue', methods=["GET"])
def get_clue():
    clue, clue_size = board.get_clue()
    clue = clue.replace('_', ' ')
    return jsonify({"clue": clue, "clue_size": clue_size})

@app.route('/api/resetgame', methods=["POST"])
def reset_game():
    global board, curr_round, session_id, log
    board = codenames.CodenamesBoard(0.25)
    curr_round = 0
    session_id = str(uuid.uuid4())
    log = ""
    return jsonify({"message": "Game reset successfully."})

@app.route('/api/gameover', methods=["GET"])
def game_over_status():
    if game_over():
        winner = board.winner()
        return jsonify({"game_over": True, "winner": winner})
    else:
        return jsonify({"game_over": False})

@app.route('/api/getscore', methods=["GET"])
def get_score():
    global board
    player_score, opponent_score = board.get_score()
    return jsonify({"player_score": player_score, "opponent_score": opponent_score})

@app.route('/', methods=['GET'])
def index():
    return send_from_directory(app.static_folder, 'index.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)