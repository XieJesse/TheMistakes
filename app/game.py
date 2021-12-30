from flask import Flask, Blueprint, request, session, render_template, redirect, g
import sqlite3, json, urllib, random
import auth

bp = Blueprint('game', __name__)

@bp.route("/play",methods=['GET', 'POST'])
@auth.login_required
def play():
    return render_template("setup.html")

@bp.route("/setup", methods=['GET','POST'])
def initialSetup():
    '''
    # outlining concerns: newDeck() is run once per session. Here, it is run so that we will a deck ready for newGame to not throw an error.
    # Whenever we want to start a new game, though, we want to return all cards, shuffle, then take them all back. We don't want to call initialSetup.
    # We want to create and call a new function called postInitSetup, that returns all cards in a deck, shuffles them, takes them all back, and starts a new game.
    '''
    newDeck()
    players = 0
    if request.method == 'POST':
        players = int(request.form['cpu_number']) + 1
    cards = drawCards(players * 2)
    newGame(players, cards)
    #playerCards = []
    #print(session["formattedCards"][0])
    # formatting the cards to be passed via jinja variables
    #for i in range(players):
    #    playerCards.append([ [cards[i*2]["value"], cards[i*2]["suit"]],  [cards[i*2+1]["value"], cards[i*2+1]["suit"]] ])

    return render_template("game.html", cards = session["formattedCards"][0], cpus = session["formattedCards"][1:])


def postInitSetup():
    """
    # TODO:
    * 1) Return all cards in a deck }
    * 2) Shuffle all cards in a deck } --> Raymond's return method, I believe, should work
    * 3) Take back all cards in a deck }
    * 4) Start a newGame --> newGame()
    """
    return render_template("game.html")

# Creates a session variable that is a list of tuples
# Here is the tuple diagram: (Cards, Card Value, Status)
# Example tuple: (["KH","5D","AC"], 17, Hit/Bust/Stay)
# TODO: Update score for each CPU properly
def newGame(playerCount, drawnCards):
    # Session variable players tracks human and cpu player stats
    session['players'] = [[[],0,""] for i in range(playerCount)]
    session["formattedCards"] = []
    for i in range(playerCount-1):
        session['players'][i][0].append(drawnCards[i*2]["code"])
        session['players'][i][0].append(drawnCards[i*2+1]["code"])
        # session['players'][i][1] += scoreCards(session['players'][i][0])
    for i in range(playerCount):
        session["formattedCards"].append([ [drawnCards[i*2]["value"], drawnCards[i*2]["suit"]], [drawnCards[i*2+1]["value"], drawnCards[i*2+1]["suit"]] ])

def reward():
    d = db.get_db()
    c = d.cursor()
    payout = 50 #can change if needed (maybe make it random)
    c.execute("SELECT * FROM USERS WHERE USERNAME = (?)", (session['username'],))
    userPoints = c.fetchone()
    if blackjack_win == "blackjack":
        c.execute("UPDATE USERS SET POINTS = (?) WHERE USERNAME = (?)", (userPoints[2]+ (1.5 * payout), session['username']))
    else:
        c.execute("UPDATE USERS SET POINTS = (?) WHERE USERNAME = (?)", (userPoints[2]+ payout, session['username']))


@bp.route("/blackjack")
def game():
    # try:
        # Game code
    # except:
        return render_template("home.html")

@bp.route("/hold")
def stay():
    session['players'][0][2] = "Stay"
    # TODO:
    # Add functionality to draw cards for house and cpus until they all either bust or stay
    # Then determine winner
    return render_template("game.html")

@bp.route("/draw")
def hit():
    drawnCard = drawCards(1)
    session['players'][0][0].append(drawnCard[0]["code"])
    session['players'][0][1] += scoreCards([drawnCard[0]])
    if session['players'][0][1] > 21:
        session['players'][0][2] = "Bust"

# player_scores will be a list.
# The first element of that list is the score of the human player. There will then be a variable number of cpu player scores.
# The last score will be the score of the house. There will always be a minimum of 2 scores.
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
        if player_scores[i] == 21:
            return "blackjack"

def cpuBehavior(players):
    for i in players[1:]:
        if i[1] > 21:
            i[2] == 'Bust'
        elif i[1] >= 17 and i[1] <= 21 and i[2] == "Hit":
            i[2] = "Stay"
        elif i[1] < 17 and i[2] == "Hit":
            drawnCard = drawCards(1)[0]
            i[0].apend(drawnCard["code"]);
            i[1] += scoreCards([drawnCard])
            if i[1] > 21:
                i[2] == "Bust"

def checkError(url):
    try:
        r = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        return r
    except requests.exceptions.RequestException:
        raise Exception("API may not be working at the moment.")

def newDeck():
    # opens up API data (API data being a randomly made deck)
    req = checkError('https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1')
    data = urllib.request.urlopen(req)
    # reads API data into variable (comes in as JSON data)
    response = data.read()
    # converts JSON data to python dictionary
    response_info = json.loads(response)
    # sets a variable deckid equal to the deck_id of the drawn deck
    deckid = response_info["deck_id"]
    deck_req = checkError('https://deckofcardsapi.com/api/deck/' + deckid + '/draw/?count=52')
    deck_data = urllib.request.urlopen(deck_req)
    deck_response = deck_data.read()
    deck_dict = json.loads(deck_response)
    session["deck"] = deck_dict["cards"] #List of dictionaries
    """
    example session['deck'] # taken from Deck of Cards API
    [
        {
            "image": "https://deckofcardsapi.com/static/img/KH.png",
            "value": "KING",
            "suit": "HEARTS",
            "code": "KH"
        },
        {
            "image": "https://deckofcardsapi.com/static/img/8C.png",
            "value": "8",
            "suit": "CLUBS",
            "code": "8C"
        }
    ]
    """

# logic error: returns empty list
# logic error status: resolved
# returns list of card dictionaries
def drawCards(numCards):
    cards = []
    if ('deck' in session.keys()):
        for i in range(numCards):
            cards.append(session['deck'][i])
        session['deck'] = session['deck'][numCards:]
    return cards

def returnCards():
    req = checkError('https://deckofcardsapi.com/api/deck/' + DECKID + '/return/')
    data = urllib.request.urlopen(req)
    #new set of cards
    deck_req = checkError('https://deckofcardsapi.com/api/deck/' + deckid + '/draw/?count=52')
    deck_data = urllib.request.urlopen(deck_req)
    deck_response = deck_data.read()
    deck_dict = json.loads(deck_response)
    session["deck"] = deck_dict["cards"]
    #returns all cards back to deck and shuffles

# cardsPlayed parameter should be a list of codes
def scoreCards(cardsPlayed):
    score = 0
    faceCards = "K, Q, J"
    for card in cardsPlayed:
        if card[0] in faceCards:
            score += 10
        if card[0] == "A" and (score + 11) < 21:
            score += 11
        else:
            score += 1
        if card[0] not in faceCards:
            score += card[0]
    return score
