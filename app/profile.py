from flask import Flask, Blueprint, request, session, render_template, redirect, g
import os, sqlite3, json, urllib
import auth
import random
from db import get_db

bp = Blueprint('profile', __name__)

@bp.route("/profile", methods=['GET', 'POST'])
@auth.login_required
def profile():
    d = get_db()
    c = d.cursor()
    c.execute("SELECT * FROM USERS WHERE USERNAME = (?)", (session['username'],))
    userData = c.fetchone()
    balance = userData[2]
    wins = userData[3]
    currColor = userData[7]
    colors = []
    pfps = []
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
        if itemList[0] == "pfp":
            pfps.append(itemList[2])
    print(pfps)
    return render_template("profile.html",username=session['username'],balance=balance,wins=wins,picture_list=pfps,color_list=colors,current_color=currColor)

@bp.route("/swap_color", methods=['GET', 'POST'])
@auth.login_required
def swap_color():
    d = get_db()
    c = d.cursor()
    c.execute("UPDATE USERS SET POINTS = (?) WHERE USERNAME = (?)", (session['username'],))

    profile()
