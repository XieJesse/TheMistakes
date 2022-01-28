from flask import Flask, Blueprint, request, session, render_template, redirect, g
import sqlite3, json, urllib, os, random
from app import auth, db
bp = Blueprint('game', __name__)

"""
# TODO:
# Resolved: Check if player busted while hitting the stay button on "game.html"
# Get postInitSetup working
# Resolved: Finish the endGame function
# Resolved: Finish the blackjack_win function, and display the winner as "You won!" or "CPUs won! You lost!" on "results.html"
# Route a button to use the postInitSetup function under the route "playAgain". The button will appear on results.html. It will render_template "game.html"
# Resolved: Make sure that, after clicking Stay or becoming Bust, players are rewarded or lose money accordingly.
# Resolved: Display the player score and the scores of each cpu on the results page, as well as the cards of the players and the cpus on the results page.
"""
@bp.route("/play",methods=['GET', 'POST'])
@auth.login_required
def play():
    try:
        d = db.get_db()
        c = d.cursor()
        c.execute("SELECT * FROM USERS WHERE USERNAME = (?)", (session['username'],))
        userData = c.fetchone()
        colors = []
        inventory_file = f"{session['username']}.txt"
        inventory_dir = "inventories"

        # Join the inventory filename to the inventories path
        inventory_path = os.path.join(inventory_dir, inventory_file)

        with open(inventory_path, "r") as inventory:
            allItems = inventory.readlines()
        for item in allItems:
            itemList = item.split("|")
            if itemList[0] == "card_color":
                colors.append(itemList[2])
        return render_template("setup.html",colors=colors)
    except:
        return render_template("login.html", error = "An issue occurred trying to play Blackjack")

@bp.route("/setup", methods=['GET','POST'])
def initialSetup():
    try:
        session["mainCol"] = "255, 43, 107"
        session["altCol"] = "0, 0, 0"
        '''
        # outlining concerns: newDeck() is run once per session. Here, it is run so that we will a deck ready for newGame to not throw an error.
        # Whenever we want to start a new game, though, we want to return all cards, shuffle, then take them all back. We don't want to call initialSetup.
        # We want to create and call a new function called postInitSetup, that returns all cards in a deck, shuffles them, takes them all back, and starts a new game.
        '''
        if "deck" in session and "deckId" in session:
            #print("bruh")
            returnCards()
        else:
            newDeck()
        players = 0
        if request.method == 'POST':
            players = int(request.form['cpu_number']) + 1
            session["mainCol"] = request.form["mainColor"]
            session["altCol"] = request.form["altColor"]
        cards = drawCards(players * 2)
        newGame(players, cards)
        #playerCards = []
        #print(session["formattedCards"][0])
        # formatting the cards to be passed via jinja variables
        #for i in range(players):
        #    playerCards.append([ [cards[i*2]["value"], cards[i*2]["suit"]],  [cards[i*2+1]["value"], cards[i*2+1]["suit"]] ])
        session["roundNumber"] = 1

        return render_template("game.html", cards = session["formattedCards"][0], cpus = session["formattedCards"][1:], round_no = session["roundNumber"], main_color = session["mainCol"], alt_color = session["altCol"])
    except:
        return render_template("login.html", error = "An issue has occurred setting up the game Blackjack")

"""
# test_cards = [("A", "DIAMONDS"), ("3", "CLUBS"), ("3", "CLUBS"), ("3", "CLUBS")]

# test_cpus = [
#    [[("A", "DIAMONDS"), ("3", "CLUBS")], False],
#    [[("A", "DIAMONDS"), ("3", "CLUBS"), ("3", "CLUBS"),("3", "CLUBS"),("3", "CLUBS")], True],
#    [[("A", "DIAMONDS"), ("3", "CLUBS"), ("3", "CLUBS"), ("3", "CLUBS")], False],
#    [[("A", "DIAMONDS"), ("3", "CLUBS"), ("3", "CLUBS"),("3", "CLUBS"),("3", "CLUBS")], True]
# ]
# test_round_no = 2

# return render_template("game.html", cards = test_cards, cpus = test_cpus, round_no = test_round_no)

# example
# session["formattedCards"] = [
# [("A", "DIAMONDS"), ("3", "CLUBS"), ("3", "CLUBS"), ("3", "CLUBS")],
# [[("A", "DIAMONDS"), ("3", "CLUBS")], False],
#[[("A", "DIAMONDS"), ("3", "CLUBS"), ("3", "CLUBS"),("3", "CLUBS"),("3", "CLUBS")], True]
# ]
"""
# Outdated comments are in triple strings
# """ Creates a session variable that is a list of tuples
# Here is the tuple diagram: (Cards, Card Value, Status)
# Example tuple: (["KH","5D","AC"], 17, Hit/Bust/Stay) """
# TODO: Update score for each CPU properly
def newGame(playerCount, drawnCards):
    # Session variable players tracks human and cpu player stats
    session['players'] = [[[],0,""] for i in range(playerCount)]
    session["formattedCards"] = []
    for i in range(playerCount):
        session['players'][i][0].append(drawnCards[i*2]["code"])
        session['players'][i][0].append(drawnCards[i*2+1]["code"])
        session['players'][i][1] = scoreCards(session['players'][i][0])
        session['players'][i][2] = "Hit"
    for i in range(playerCount):
        if i == 0:
            session["formattedCards"].append([(drawnCards[i*2]["value"], drawnCards[i*2]["suit"]), (drawnCards[i*2+1]["value"], drawnCards[i*2+1]["suit"])])
        else:
            session["formattedCards"].append([ [(drawnCards[i*2]["value"], drawnCards[i*2]["suit"]), (drawnCards[i*2+1]["value"], drawnCards[i*2+1]["suit"])], True ])
    #print(session["players"])

def rewardCalc():
    payout = 70 #can change if needed (maybe make it random)
    winner = blackjackWin([x[1] for x in session["players"]])
    # blackjackWin(list_of_player_scores)[1]
    if (winner[0] == True and winner[1] == True):
        payout = 100
    elif winner[0] == True:
        payout = 70
    elif winner[1] == True:
        payout = 0
    else:
        payout = 0
    return payout

def reward():
    d = db.get_db()
    c = d.cursor()
    payout = rewardCalc()
    c.execute("SELECT * FROM USERS WHERE USERNAME = (?)", (session['username'],))
    userPoints = c.fetchone()
    if payout > 0:
        c.execute("SELECT * FROM USERS WHERE USERNAME = (?)", (session['username'],))
        userData = c.fetchone()
        wins = userData[3]
        c.execute("UPDATE USERS SET WINS = (?) WHERE USERNAME = (?)", (wins+1, session['username']))
    c.execute("UPDATE USERS SET POINTS = (?) WHERE USERNAME = (?)", (userPoints[2] + payout, session['username']))
    d.commit()


def endGame():
    isAllHit = True
    while (isAllHit):
        isAllHit = False
        cpuBehavior(session["players"])
        for i in session["players"][1:]:
            if i[2] == "Hit":
                isAllHit = True
                break

@bp.route("/hold")
def stay():
    try:
        if session["players"][0][1] > 21:
            session['players'][0][2] = "Bust"
            endGame()
            winner = blackjackWin([x[1] for x in session["players"]])
            result = ""
            if winner[1]:
                result += "Blackjack "
            if winner[0]:
                result += "Victory"
            else:
                result += "Defeat"
            reward()
            cpuHands = session["formattedCards"][1:]
            for hand in cpuHands:
                hand.remove(False)
            print(cpuHands)
            print(cpuHands[0])
            # cards and values are debugger jinja variables
            return render_template("results.html", outcome = result, pointReward = rewardCalc(), msg = "You busted!", playerHand = session["formattedCards"][0], cpuHands = cpuHands, playerValue = [session["players"][0][1]] , cpuValues = [x[1] for x in session["players"][1:]])
        else:
            session['players'][0][2] = "Stay"
            endGame()
            winner = blackjackWin([x[1] for x in session["players"]])
            result = ""
            if winner[1]:
                result += "Blackjack "
            if winner[0]:
                result += "Victory!"
            else:
                result += "Defeat"
            reward()
            cpuHands = session["formattedCards"][1:]
            for hand in cpuHands:
                hand.remove(False)
            print(cpuHands)
            print(cpuHands[0])
            # cards and values are debugger jinja variables
            return render_template("results.html", outcome = result, pointReward = rewardCalc(), msg = "You stood!", playerHand = session["formattedCards"][0], cpuHands = cpuHands, playerValue = [session["players"][0][1]] ,cpuValues = [x[1] for x in session["players"][1:]])
    except:
        return render_template("login.html", error = "An issue occurred with the hit button")

@bp.route("/draw")
def hit():
    try:
        if session['players'][0][1] > 21:
            #print(session['players'][0][1])
            session['players'][0][2] = "Bust"
            endGame()
            winner = blackjackWin([x[1] for x in session["players"]])
            result = ""
            if winner[1]:
                result += "Blackjack "
            if winner[0]:
                result += "Victory!"
            else:
                result += "Defeat"
            reward()
            cpuHands = session["formattedCards"][1:]
            for hand in cpuHands:
                hand.remove(False)
            print(cpuHands)
            print(cpuHands[0])
            # cards and values are debugger jinja variables
            return render_template("results.html", outcome = result, pointReward = rewardCalc(), msg = "You busted!", playerHand = session["formattedCards"][0], cpuHands = cpuHands, playerValue = [session["players"][0][1]] ,cpuValues = [x[1] for x in session["players"][1:]])
        else:
            session["roundNumber"] += 1
            drawnCard = drawCards(1)
            session['players'][0][0].append(drawnCard[0]["code"])
            #print(session['players'][0][1])
            session['players'][0][1] = scoreCards(session['players'][0][0])
            session["formattedCards"][0].append( (drawnCard[0]["value"], drawnCard[0]["suit"]) )
            session["players"][0][2] = "Hit"
            # cpuBehavior will alter the session variables players and formattedCards accordingly, based on card scores taken from the players session variable
            cpuBehavior(session["players"])
            return render_template("game.html", cards = session["formattedCards"][0], cpus = session["formattedCards"][1:], round_no = session["roundNumber"], main_color = session["mainCol"], alt_color = session["altCol"])
    except:
        return render_template("login.html", error = "An issue occurred with the hit button")


# player_scores will be a list.
# The first element of that list is the score of the human player. There will then be a variable number of cpu player scores.
# The last score will be the score of the house. There will always be a minimum of 2 scores.
# Example: [20, 4, 17, 23, 21]
# Returns list of tuples, where the first element of each tuple is the player number
# (0 being human, len-1 being cpu, everything else being cpu)
# and the second element will be the player's score. Everyone over 21 will be removed
# from the final list. The player with the highest score will win. If two people tie
# or if the list of tuples is empty (meaning everyone busted) then no one will be awarded coins
# returns True if player won. False if cpus won
def blackjackWin(player_scores):
    modified_player_scores = []
    isPlayerWinner = False
    isBlackJack = False
    for i in range(len(player_scores)):
        if player_scores[i] < 22:
            modified_player_scores.append((i, player_scores[i]))
    if (len(modified_player_scores) > 0):
        values = [x[1] for x in modified_player_scores]
        winner = values.index(max(values))
        if (len(modified_player_scores) > 0 and modified_player_scores[winner][0] == 0):
            isPlayerWinner = True
        if(values[winner] == 21):
            isBlackJack = True
    return (isPlayerWinner, isBlackJack)

def cpuBehavior(players):
    for i in range(len(players[1:])):
        if players[i+1][1] > 21:
            players[i+1][2] = 'Bust'
            session["formattedCards"][i+1][1] = False
        elif players[i+1][1] >= 17 and players[i+1][1] <= 21:
            players[i+1][2] = "Stay"
            session["formattedCards"][i+1][1] = False
        elif players[i+1][1] < 17:
            drawnCard = drawCards(1)
            players[i+1][0].append(drawnCard[0]["code"]);
            players[i+1][1] = scoreCards(players[i+1][0])
            players[i+1][2] = "Hit"
            session["formattedCards"][i+1][0].append( (drawnCard[0]["value"], drawnCard[0]["suit"]) )
            session["formattedCards"][i+1][1] = True


def checkError(url):
    try:
        r = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        return r
    except requests.exceptions.RequestException:
        return render_template("login.html", error = "An API error has occurred. Please try again later.")

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
    session["deckId"] = deckid
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
    checkError('https://deckofcardsapi.com/api/deck/' + session["deckId"] + '/return/')
    req = checkError('https://deckofcardsapi.com/api/deck/' + session["deckId"] + '/shuffle/')
    data = urllib.request.urlopen(req)
    #new set of cards
    deck_req = checkError('https://deckofcardsapi.com/api/deck/' + session["deckId"] + '/draw/?count=52')
    deck_data = urllib.request.urlopen(deck_req)
    deck_response = deck_data.read()
    deck_dict = json.loads(deck_response)
    session["deck"] = deck_dict["cards"]
    #returns all cards back to deck and shuffles

# cardsPlayed parameter should be a list of codes
def scoreCards(cardsPlayed):
    score = 0
    faceCards = "K, Q, J, 0"
    for card in cardsPlayed:
        if card[0] in faceCards:
            score += 10
        elif card[0] == "A":
            if (score + 11) < 22:
                score += 11
            else:
                score += 1
        elif card[0] not in faceCards:
            score += int(card[0])
    return score
