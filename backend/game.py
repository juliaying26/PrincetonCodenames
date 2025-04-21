from flask import Flask, redirect, request, jsonify, send_from_directory, abort
import codenames
import setup
import uuid

app = Flask(__name__, template_folder='../frontend', static_folder='../frontend/dist')

board = codenames.CodenamesBoard(0.25)
rounds = 2
curr_round = 0
session_id = str(uuid.uuid4())
log = ""

# # Initialize persistent log display
# display(HTML("""
# <div id="game-area">
#   <div id="log" style="font-family:monospace; white-space:pre-wrap; padding:10px; background:#f9f9f9; border:1px solid #ddd; border-radius:8px; margin-bottom:20px;"></div>
#   <div id="input-area"></div>
# </div>
# """))

def append_to_log(message):
    global log
    log += message + "\n"


def check_game_over():
    global curr_round
    if board.game_over:
        append_to_log("<b style='color:red;'>Game Over!</b>")
        return True
    return False

@app.route('/api/opponentplays', methods=['POST'])
def opposing_team_round():
    if check_game_over():
        return
    append_to_log("<h2>--------OPPONENT ROUND--------</h2>")
    clue, clue_size = board.opponent_get_clue()
    append_to_log(f'Clue: <i>{clue}</i>, {clue_size} (up to {clue_size+1} guesses)')
    msg = board.opponent_guess(clue, clue_size)
    append_to_log(msg)
    my_team_clue()

# output.register_callback(f'notebook.submitGuesses_{session_id}', submit_guesses)

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
    # clear_output()
    # display(Javascript('document.getElementById("input-area").innerHTML = "";'))

    if check_game_over():
        return jsonify({"game_over": True})

    print("hit /api/guessword")  # make sure this shows up
    data = request.get_json()
    print("data received:", data)  # see what the frontend sent
    guess = data.get('word')

    append_to_log(f"<p>Your guesses: {guess}</p>")
    msg = board.team_guesses(guess)
    append_to_log(msg)
    curr_round += 1
    return jsonify({"message": msg})

@app.route('/api/getclue', methods=["GET"])
def get_clue():
    clue, clue_size = board.get_clue()
    return jsonify({"clue": clue, "clue_size": clue_size})

@app.route('/', methods=['GET'])
def index():
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)