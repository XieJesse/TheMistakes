from flask import Flask, Blueprint, request, session, render_template, redirect, g
import os, sqlite3, json, urllib
import auth
import random
from db import get_db

bp = Blueprint('leaderboard', __name__)

@bp.route("/leaderboard", methods=['GET', 'POST'])
@auth.login_required
def leaderboard():
    d = get_db()
    c = d.cursor()
    c.execute("SELECT * FROM USERS")
    users = c.fetchall()
    players = []
    for user in users:
        # add username, wins, points to list
        players.append([user[0],user[3],user[2]])
    return render_template("leaderboard.html",players=players)
