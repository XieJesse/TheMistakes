from flask import Flask, request, session, render_template, redirect
import sqlite3
import json
import db

app = Flask(__name__)

# Misc Render Function for testing templating
@app.route("/", methods=['GET', 'POST'])
def test():

    # SETUP TEST
    # test_colors = ["#000000", "#f5493d", "#318fe0", "#78a6ce"]
    # test_rgb = ["238,58,58", "28,28,28", "255,255,255", "78, 78, 245"]
    # return render_template("setup.html", colors=test_rgb)

    # GAME TEST
    # test_cards = [["A", "DIAMONDS"], ["3", "CLUBS"], ]
    # test_cpus = [[["A", "DIAMONDS"], ["3", "CLUBS"]], [["A", "DIAMONDS"], ["3", "CLUBS"], ["3", "CLUBS"]]]

    # return render_template("game.html", cards = test_cards, cpus = test_cpus)
    
    # LEADERBOARD TEST
    # d = db.get_db()
    # c = d.cursor()

    # GET_PLAYERS = """SELECT * FROM USERS"""

    # c.execute(GET_PLAYERS)

    # test_players = c.fetchall()
    # print(test_players[0]['profile_picture'])

    # return render_template("leaderboard.html", players=test_players)

    # SHOP TEST

    d = db.get_db()
    c = d.cursor()
    
    c.execute("SELECT * FROM SHOP")

    test_items = c.fetchall()
    return render_template("shop.html", items=test_items)

if __name__ == "__main__":
    app.debug = True
    app.run()
