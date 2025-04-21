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

def append_to_log(message):
    # Send a JS command to append to the #log div
    js = f"""
    const logDiv = document.getElementById("log");
    const newEntry = document.createElement("div");
    newEntry.innerHTML = `{message}`;
    logDiv.appendChild(newEntry);
    """
    # display(Javascript(js))


def check_game_over():
    global curr_round
    if board.game_over:
        append_to_log("<b style='color:red;'>Game Over!</b>")
        return True
    return False

def my_team_clue():
    global curr_round
    # clear_output()
    # display(Javascript('document.getElementById("input-area").innerHTML = "";'))

    if check_game_over():
        return

    clue, clue_size = board.get_clue()
    words_on_board = board.remaining_cards()
    options = words_on_board + ['no additional guesses this round']

    append_to_log(f"<h2>--------YOUR ROUND--------</h2> Clue: <i>{clue}</i>, {clue_size} (up to {clue_size+1} guesses)")

    # Build HTML dropdowns
    dropdowns_html = ""
    for i in range(clue_size + 1):
        dropdowns_html += f"""
        <label for="guess{i}">Guess {i+1}:</label>
        <select id="guess{i}">
            {''.join(f'<option value="{word}">{word}</option>' for word in options)}
        </select><br>
        """

    # HTML for the form
    html_code = f"""
    <div>
        <p><b>Clue:</b> {clue} (You may guess up to {clue_size + 1} words)</p>
        {dropdowns_html}
        <button id="submit-btn">Submit Guesses</button>
    </div>
    <script>
    (function() {{
        const btn = document.getElementById("submit-btn");
        if (btn) {{
            btn.onclick = function() {{
                let guesses = [];
                for (let i = 0; i < {clue_size + 1}; i++) {{
                    guesses.push(document.getElementById('guess' + i).value);
                }}
                google.colab.kernel.invokeFunction(
                    'notebook.submitGuesses_{session_id}',
                    [guesses],
                    {{}}
                );
            }};
        }}
    }})();
    </script>
    """

    # Inject into the input area using HTML instead of Javascript
    # display(Javascript('document.getElementById("input-area").innerHTML = "";'))  # clear previous input
    # display(HTML(f'<div id="form-wrapper">{html_code}</div>'))

# Python function to be triggered from JS
def submit_guesses(guesses):
    global curr_round
    append_to_log(f"<p>Your guesses: {guesses}</p>")
    msg = board.team_guesses(guesses)
    append_to_log(msg)
    curr_round += 1
    opposing_team_round()

# output.register_callback(f'notebook.submitGuesses_{session_id}', submit_guesses)

def opposing_team_round():
    if check_game_over():
        return
    append_to_log("<h2>--------OPPONENT ROUND--------</h2>")
    clue, clue_size = board.opponent_get_clue()
    append_to_log(f'Clue: <i>{clue}</i>, {clue_size} (up to {clue_size+1} guesses)')
    msg = board.opponent_guess(clue, clue_size)
    append_to_log(msg)
    my_team_clue()

@app.route('/api/ping')
def ping():
    return jsonify({"message": "pong"})

@app.route('/', methods=['GET'])
def index():
    my_team_clue()
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)