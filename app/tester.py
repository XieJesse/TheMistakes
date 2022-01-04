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
    test_cards = [("A", "DIAMONDS"), ("3", "CLUBS"), ("3", "CLUBS"), ("3", "CLUBS")]

    # The first card within each sublist is displayed.
    # A list of cpus containing sublists for each CPU
    # Each sublist contains a list of card tuples, and a boolean 
    # The card tuples can be lists, but tuples help with visibility
    # The boolean tells whether the CPU hit (true) or stood (false) in the last round
    test_cpus = [
        [[("A", "DIAMONDS"), ("3", "CLUBS")], False],
        [[("A", "DIAMONDS"), ("3", "CLUBS"), ("3", "CLUBS"),("3", "CLUBS"),("3", "CLUBS")], True],
        [[("A", "DIAMONDS"), ("3", "CLUBS"), ("3", "CLUBS"), ("3", "CLUBS")], False],
        [[("A", "DIAMONDS"), ("3", "CLUBS"), ("3", "CLUBS"),("3", "CLUBS"),("3", "CLUBS")], True]
    ]

    # Current round number
    test_round_no = 2

    # Card Colors
    test_main = "255, 43, 107"
    test_alt = "210, 240, 252"

    return render_template("game.html", cards = test_cards, cpus = test_cpus, round_no = test_round_no, main_color = test_main, alt_color = test_alt)
    
    # LEADERBOARD TEST
    # d = db.get_db()
    # c = d.cursor()

    # GET_PLAYERS = """SELECT * FROM USERS"""

    # c.execute(GET_PLAYERS)

    # test_players = c.fetchall()
    # print(test_players[0]['profile_picture'])

    # return render_template("leaderboard.html", players=test_players)

    # SHOP TEST
    # d = db.get_db()
    # c = d.cursor()
    
    # c.execute("SELECT * FROM SHOP")

    # test_items = c.fetchall()
    # return render_template("shop.html", items=test_items)

    # Profile Test

    # test_username = "johndoe"
    # test_bal = 10000
    # test_wins = 999

    # Lists of profile pictures (with the current pfp at index 0)
    # test_pfps = ["https://cdn.discordapp.com/attachments/803649184887472148/913649895276163082/citygirl_recolor_eyes.png", "https://cdn.discordapp.com/attachments/803649184887472148/926572649277181982/mogumo_1.1.png", ""]
    
    # The current color the user is using
    # test_current_color = "214, 0, 79"
    # List of colors within the user's inventory 
    # test_colors = ["0,0,0", "20,20,20", "214, 0, 79", "251, 143, 255"]

    # return render_template("profile.html", username = test_username, balance = test_bal, wins=test_wins, picture_list = test_pfps, current_color = test_current_color, color_list = test_colors)

    # Home Test

    # test_username = "johndoe"
    # test_bal = 10000
    # test_wins = 999
    # test_current_color = "214, 0, 79"
    # test_pfp = "https://cdn.discordapp.com/attachments/803649184887472148/913649895276163082/citygirl_recolor_eyes.png"

    # return render_template("home.html", username = test_username, balance = test_bal, wins=test_wins, current_color = test_current_color, profile_picture = test_pfp)

    # Result Test

    # test_hand = [("A", "DIAMONDS"), ("3", "CLUBS"), ("3", "CLUBS"), ("3", "CLUBS")]
    # test_cpus = [
    #     [("A", "DIAMONDS"), ("3", "CLUBS")],
    #     [("A", "DIAMONDS"), ("3", "CLUBS"), ("3", "CLUBS"),("3", "CLUBS"),("3", "CLUBS")],
    #     [("A", "DIAMONDS"), ("3", "CLUBS"), ("3", "CLUBS"), ("3", "CLUBS")],
    #     [("A", "DIAMONDS"), ("3", "CLUBS"), ("3", "CLUBS"),("3", "CLUBS"),("3", "CLUBS")]
    # ]
    # test_values = [0,1,2,3,4]

    # test_reward = {
    #     "data" : "245, 0, 139", 
    #     "type" : "color",
    #     "name" : "Hot Pink"
    # }

    # test_reward = {
    #     "data" : "https://cdn.discordapp.com/attachments/803649184887472148/926572649277181982/mogumo_1.1.png", 
    #     "type" : "image",
    #     "name" : ""
    # }

    # return render_template("results.html", playerHand = test_hand, cpuHands = test_cpus, cpuValues=test_values, reward = test_reward)

if __name__ == "__main__":
    app.debug = True
    app.run()
