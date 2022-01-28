from flask import Flask, Blueprint, request, session, render_template, redirect, g
import os, sqlite3, json, urllib
import random
from app import auth
from app.db import get_db

bp = Blueprint('profile', __name__)

@bp.route("/profile", methods=['GET', 'POST'])
@auth.login_required
def profile():
    try:
        d = get_db()
        c = d.cursor()
        c.execute("SELECT * FROM USERS WHERE USERNAME = (?)", (session['username'],))
        userData = c.fetchone()
        balance = userData[2]
        wins = userData[3]
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
        return render_template("profile.html",username=session['username'],balance=balance,wins=wins,picture_list=pfps,color_list=colors)
    except:
        return render_template("login.html", error = "An issue has occurred with the profile page")

@bp.route("/swap_pfp", methods=['GET', 'POST'])
@auth.login_required
def swap_pfp():
    try:
        if request.method == 'POST':
            newImg = request.form['img_url']
            d = get_db()
            c = d.cursor()
            # set pfp in database
            c.execute("UPDATE USERS SET PROFILE_PICTURE = (?) WHERE USERNAME = (?)", (newImg,session['username']))
            d.commit()
            inventory_file = f"{session['username']}.txt"
            inventory_dir = "inventories"

            #edit inventory item order
            inventory_path = os.path.join(inventory_dir, inventory_file)

            #rewrite inventory so that pfp is first
            with open(inventory_path, "r+") as inventory:
                allItems = inventory.readlines()
                index = 0
                for line in allItems:
                    lineList = line.split("|")
                    if lineList[2].strip() == newImg.strip():
                        index = len(line)
                        inventory.seek(0)
                        inventory.write(line)
                inventory.seek(index)
                for line in allItems:
                    lineList = line.split("|")
                    if lineList[2].strip() != newImg.strip():
                        inventory.write(line)

        return profile()
    except:
        return render_template("login.html", error = "An issue has occurred with swapping profiles")
