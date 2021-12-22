from flask import Flask, Blueprint, request, session, render_template, redirect, g
import sqlite3, json, urllib, random

bp = Blueprint('game', __name__)

@bp.route("/setup", methods=['GET','POST'])
def initialSetup():
    newGame()

@bp.route("/blackjack")
def game():
    # try:
        # Game code
    # except:
        return render_template("home.html")

def cpuBehavior(players):
    for i in players:
        if i[1] > 21:
            i[2] == "Bust"
        elif i[1] >= 17 and i[1] <= 21 and i[2] == "Hit":
            i[2] = "Stay"
        elif i[1] < 17 and i[2] == "Hit":
            drawnCard = drawCards(1)[0]
            i[0] += drawnCard["code"][0];
            i[1] += scoreCards([drawnCard])



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

# Creates a session variable that is a list of tuples
# Here is the tuple diagram: (Cards, Card Value, Status)
# Example tuple: ("K5A", 17, Hit/Bust/Stay)
def newGame(playerCount):
    # Session variable players tracks human and cpu player stats
    session['players'] = [["",0,""] for i in range(playerCount)]
    # Session variable house tracks house player
    session['house'] = [["",0,""]]

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

def drawCards(numCards):
    cards = []
    if ('deck' in session.keys()):
        for i in range(numCards):
            cards.append(session['deck'][i])
        session['deck'] = session[deck][numCards]
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
