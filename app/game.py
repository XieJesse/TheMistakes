from flask import Flask, Blueprint, request, session, render_template, redirect, g
import sqlite3, json, urllib

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
    # for i in range(len(player_scores)):
    #     if player_scores[i] < 22:
            # modified_player_scores.append((i, player_scores will be a lislayer_scores[i]))
if the list of tuples is empty (meaning everyone busted) then no one will be awarded coins
def blackjack_win(player_scores):
    modified_player_scores = []
    for i in range(len(player_scores)):
        if player_scores[i] < 22:
            modified_player_scores.append((i, player_scores[i]))

# player_scores will be a list.
# The first element of that list is the score of the human player.
# There will then be a variable number of cpu player scores.
# The last score will be the score of the house.
# There will always be a minimum of 2 scores.
# Example: [20, 4, 17, 23, 21]
# Returns list of tuples, where the first element of each tuple is the player number
# (0 being human, len-1 being cpu, everything else being cpu)
# and the second element will be the player's score. Everyone over 21 will be removed
# from the final list. The
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
    deck_req = urllib.r    data = urllib.request.urlopen(req)
    #returns all cards back to deck and shufflesequest.Request('https://deckofcardsapi.com/api/deck/' + deckid + '/draw/?count=52', headers={'User-Agent': 'Mozilla/5.0'})
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

def shuffle():
    req = urllib.request.Request('https://deckofcardsapi.com/api/deck/' + deckid + '/pile/<<pile_name>>/shuffle/', headers={'User-Agent': 'Mozilla/5.0'})
    data = urllib.request.urlopen(req)
    response = data.read()
    deck_dict = json.loads(response)

def returnCards():
    req = urllib.request.Request('https://deckofcardsapi.com/api/deck/' + DECKID + '/return/', headers={'User-Agent': 'Mozilla/5.0'})
    data = urllib.request.urlopen(req)
    #returns all cards back to deck and shuffles
