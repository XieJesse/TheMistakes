from flask import Flask, Blueprint, request, session, render_template, redirect, g
import os, sqlite3, json, urllib, random
from app import auth
from app.db import get_db

bp = Blueprint('leaderboard', __name__)

@bp.route("/leaderboard", methods=['GET', 'POST'])
@auth.login_required
def leaderboard():
    d = get_db()
    c = d.cursor()
    players = []
    c.execute("SELECT WINS FROM USERS")
    wins = c.fetchall()
    x = []
    for win in wins:
        x.append(win[0])
    users = sort(x)
    for user in users:
        # add username, wins, points to list
        players.append([user[0],user[3],user[2],user[4]])
    return render_template("leaderboard.html",players=players)

def sort(wins):
    temp = []
    users = []
    d = get_db()
    c = d.cursor()
    for i in range(len(wins)):
        highest_wins = max(wins)
        wins.remove(highest_wins)
        c.execute("SELECT * FROM USERS WHERE WINS = (?)", (highest_wins,))
        temp += (c.fetchall())
    for u in temp:
        if u not in users:
            users.append(u)
    return users
