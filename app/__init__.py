from flask import Flask, session, render_template, redirect
import sqlite3
import json
import urllib

app = Flask(__name__)

DB_FILE="highsteaks.db"

db = sqlite3.connect(DB_FILE, check_same_thread=False) #open if file exists, otherwise create
c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events

create = "CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT, points INTEGER, wins INTEGER, losses INTEGER, activePFP TEXT) " # create users table
c.execute((create))
create = "CREATE TABLE IF NOT EXISTS items (name TEXT, imageUrl TEXT, owner TEXT) " # create items table
c.execute((create))
create = "CREATE TABLE IF NOT EXISTS market (name TEXT, imageUrl TEXT, price INTEGER) " # create market table
c.execute((create))

db.commit() #save changes to db

# Homepage render function
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form('username')
        password = request.form('password')
        if username = "":
            return render_template("register.html")
        if password = "":
            return render_template("register.html")
        c.execute("SELECT * FROM users WHERE username = (?)", (username,))
        existingUsername = c.fetchall()
        if len(existingUsername) > 0:
             return render_template("register.html")
        command = "INSERT INTO TABLE users (?,?,0,0,0,?)",(username,password,https://englishclassviaskype.com/wp-content/uploads/2019/03/Common-mistakes-in-English-to-avoid.png)
        c.execute(command)
        db.commit()
        home()
    return render_template("register.html")

# player_scores will be a list.
# The first element of that list is the score of the human player.
# There will then be a variable number of cpu player scores.
# The last score will be the score of the house.
# There will always be a minimum of 2 scores.
# Example: [20, 4, 17, 23, 21]
# Returns list of tuples, where the first element of each tuple is the player number
# (0 being human, len-1 being cpu, everything else being cpu)
# and the second element will be the player's score. Everyone over 21 will be removed
# from the final list. The player with the highest score will win. If two people tie
# or if the list of tuples is empty (meaning everyone busted) then no one will be awarded coins
def blackjack_win(player_scores):
    modified_player_scores = []
    for i in range(len(player_scores)):
        if player_scores[i] < 22:
            modified_player_scores.append((i, player_scores[i]))

def newDeck():
    # opens up API data (API data being a randomly made deck)
    req = urllib.request.Request('https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1', headers={'User-Agent': 'Mozilla/5.0'}) #change deck count for more decks of 52
    data = urllib.request.urlopen(req)
    # reads API data into variable (comes in as JSON data)
    response = data.read()
    # converts JSON data to python dictionary
    response_info = json.loads(response)
    # sets a variable deckid equal to the deck_id of the drawn deck
    deckid = response_info["deck_id"]
    return deckid

def drawCards(id):
    data = urllib.request.urlopen('https://deckofcardsapi.com/api/deck/' + id + '/draw/?count=2')
    response = data.read()
    response_info = json.loads(response)
    cards = response_info["cards"]

if __name__ == "__main__":
    app.debug = True
    app.run()
