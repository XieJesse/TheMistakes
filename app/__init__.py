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
def hello_user():
    return "who arrr you?"

def newDeck():
    # opens up API data (API data being a randomly made deck)
    data = urllib.request.urlopen('https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1')
    # reads API data into variable (comes in as JSON data)
    response = data.read()
    # converts JSON data to python dictionary
    response_info = json.loads(response)
    # sets a variable deckid equal to the deck_id of the drawn deck
    deckid = response_info["deck_id"]

def drawCards(id):
    data = urllib.request.urlopen('https://deckofcardsapi.com/api/deck/' + id '/draw/?count=2')

if __name__ == "__main__":
    app.debug = True
    app.run()
