from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import codenames
import setup
import uuid


app = Flask(__name__, template_folder='../frontend', static_folder='../frontend/dist')
CORS(app)

board = codenames.CodenamesBoard(0.25)
session_id = str(uuid.uuid4())

def game_over():
    if board.game_over:
        return True
    return False

def turn_over(guess_number, msg):
    if not game_over() and 'assassin' not in msg:
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
    data = request.get_json()
    guess = data.get('word')
    guess_number = data.get('guess_number')
    
    msg = board.team_guesses(guess)
    if extra_guess(guess_number, msg):
        return jsonify({"message": msg + "\n" + "You get an extra guess!"})
    if turn_over(guess_number, msg):
        return jsonify({"message": msg + "\n" + "Your turn is over. Please wait for the other team to play."})
    
    return jsonify({"message": msg})

@app.route('/api/opponentplay', methods=['POST'])
def opponent_play():
    clue, clue_size = board.opponent_get_clue()
    msg = board.opponent_guess(clue, clue_size)
    clue = clue.replace('_', ' ')
    print(msg)
    return jsonify({"message": msg, "clue": clue, "clue_size": clue_size})

@app.route('/api/getclue', methods=["GET"])
def get_clue():
    clue, clue_size = board.get_clue()
    clue = clue.replace('_', ' ')
    return jsonify({"clue": clue, "clue_size": clue_size})

@app.route('/api/resetgame', methods=["POST"])
def reset_game():
    global board, session_id
    board = codenames.CodenamesBoard(0.25)
    session_id = str(uuid.uuid4())
    return jsonify({"message": "Game reset successfully."})

@app.route('/api/getscore', methods=["GET"])
def get_score():
    global board
    player_score, opponent_score = board.get_score()
    return jsonify({"player_score": player_score, "opponent_score": opponent_score})

@app.route('/', methods=['GET'])
def index():
    return send_from_directory(app.static_folder, 'index.html')


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port)