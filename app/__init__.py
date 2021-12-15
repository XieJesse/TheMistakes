from flask import Flask, request, session, render_template, redirect
import sqlite3
import json
import urllib
from os import urandom

app = Flask(__name__)
app.secret_key = urandom(32)

DB_FILE="highsteaks.db"

db = sqlite3.connect(DB_FILE, check_same_thread=False) #open if file exists, otherwise create
c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events

create_users = '''CREATE TABLE IF NOT EXISTS USERS(
                USERNAME TEXT UNIQUE,
                PASSWORD TEXT,
                POINTS INTEGER,
                WINS INTEGER,
                LOSSES INTEGER,
                PROFILE_PICTURE TEXT,
                PROFILE_BACKGROUND TEXT,
                CARD_COLOR TEXT,
                INVENTORY TEXT)'''

create_market = '''CREATE TABLE IF NOT EXISTS market (
                NAME TEXT,
                IMAGE_URL TEXT,
                PRICE INTEGER)''' # create market table

c.execute(create_users)
c.execute(create_market)

db.commit() #save changes to db

def is_logged_in():
    return 'username' in session.keys()

@app.route("/play",methods=['GET', 'POST'])
def play():
    return render_template("play.html")

# Homepage render function
@app.route("/", methods=['GET', 'POST'])
def home():
    print(newDeck())
    if is_logged_in():
        return render_template("home.html")
    else:
        return render_template("login.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Check if the username / password is empty
        if not username or not password: # Strings can be converted to booleans (Empty Strings = False)
            return render_template("register.html", error = "Password / username must not be empty")

        # Check if there are any occurences of the username in the database already
        c.execute("SELECT * FROM USERS WHERE USERNAME = (?)", (username,))
        existing_username = c.fetchone()

        if existing_username:
             return render_template("register.html", error = "Username is already taken.")

        userInfo = [username,password,0,0,0,"","#000000","#FFFFFF",username+".txt"]
        c.execute("INSERT INTO USERS VALUES(?,?,?,?,?,?,?,?,?)", userInfo)
        db.commit()

        inventory = open("inventories/"+username+".txt","w")
        inventory.write("card_color,#000000")
        inventory.write("\n")
        inventory.write("profile_background,#FFFFFF")
        inventory.write("\n")

        session['username'] = username
        return redirect("/")
    else:
        return render_template("register.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form('username')
        password = request.form('password')

        # Check if username is in the database
        c.execute("SELECT * FROM USERS WHERE USERNAME = (?)", (username,))
        existing_username = c.fetchone()

        if not existing_username:
            return render_template("login.html", error = "The username does not exist.")

        # Check if password matches password of inputted user
        if existing_username[1] != password:
            return render_template("login.html", error = "The password is incorrect")

        session['username'] = username
        return redirect("/")
    else:
        return render_template("login.html")

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

def blackjackWin(player_scores):
    modified_player_scores = []
    for i in range(len(player_scores)):
        if player_scores[i] < 22:
            modified_player_scores.append((i, p# player_scores will be a lislayer_scores[i]))

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
    deck_req = urllib.request.Request('https://deckofcardsapi.com/api/deck/' + deckid + '/draw/?count=52', headers={'User-Agent': 'Mozilla/5.0'})
    deck_data = urllib.request.urlopen(deck_req)
    deck_response = deck_data.read()
    deck_dict = json.loads(deck_response)
    session["deck"] = deck_dict["cards"] #Dictionary of lists of dictionary

def drawCards():
    deck_req = urllib.request.Request('https://deckofcardsapi.com/api/deck/' + deckid + '/draw/?count=52', headers={'User-Agent': 'Mozilla/5.0'})
    deck_data = urllib.request.urlopen(deck_req)
    deck_response = deck_data.read()
    deck_dict = json.loads(deck_response)
    return deck_dict #Dictionary of lists of dictionary

def returnCards():
    req = urllib.request.Request('https://deckofcardsapi.com/api/deck/' + DECKID + '/return/', headers={'User-Agent': 'Mozilla/5.0'})
    data = urllib.request.urlopen(req)
    #returns all cards back to deck and shuffles

if __name__ == "__main__":
    app.debug = True
    app.run()
