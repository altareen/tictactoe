###
#-------------------------------------------------------------------------------
# application.py
#-------------------------------------------------------------------------------
#
# Author:       Alwin Tareen
# Created:      Dec 20, 2020
#
# Venv setup:       python3 -m venv venv
# Venv activation:  source venv/bin/activate
#
# Check if flask is installed:  python -m flask --version
# If flask is not installed:    pip install Flask
#                               pip install flask-session
#
# Set variable: export FLASK_APP="application.py"
# Execution:    flask run
# Conclusion:   deactivate
#
# This program implements a tic-tac-toe game in the browser.
#
##

from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session
from tempfile import mkdtemp

app = Flask(__name__)

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = b'\x7fR\xc8\x933\n\xea\x90\xa6\x8c\x12\xd6r#gO'
Session(app)

# Set the secret key to some random bytes. Keep this really secret!
#app.secret_key = b'\x7fR\xc8\x933\n\xea\x90\xa6\x8c\x12\xd6r#gO'

@app.route("/")
def index():
    if "board" not in session:
        session["board"] = [[None, None, None], [None, None, None], [None, None, None]]
        session["turn"] = "X"

    return render_template("game.html", game=session["board"], turn=session["turn"])


@app.route("/play/<int:row>/<int:col>")
def play(row, col):
    # Place a mark on the playing board
    session["board"][row][col] = session["turn"]

    # Check for a game winning condtion
    mark = session["turn"]
    if session["board"][0] == [mark, mark, mark] or session["board"][1] == [mark, mark, mark] or \
    session["board"][2] == [mark, mark, mark] or \
    [session["board"][0][0], session["board"][1][0], session["board"][2][0]] == [mark, mark, mark] or \
    [session["board"][0][1], session["board"][1][1], session["board"][2][1]] == [mark, mark, mark] or \
    [session["board"][0][2], session["board"][1][2], session["board"][2][2]] == [mark, mark, mark] or \
    [session["board"][0][0], session["board"][1][1], session["board"][2][2]] == [mark, mark, mark] or \
    [session["board"][0][2], session["board"][1][1], session["board"][2][0]] == [mark, mark, mark]:
        return render_template("victory.html", game=session["board"], turn=session["turn"])

    # Check for a cat's game
    if None not in session["board"][0] and None not in session["board"][1] and \
    None not in session["board"][2]:
        return render_template("catsgame.html", game=session["board"])
    
    # Switch to the other player's turn
    if session["turn"] == "X":
        session["turn"] = "O"
    elif session["turn"] == "O":
        session["turn"] = "X"

    return redirect(url_for("index"))


@app.route("/reset")
def reset():
    #del session["board"]
    session["board"] = [[None, None, None], [None, None, None], [None, None, None]]
    session["turn"] = "X"
    return redirect(url_for("index"))

