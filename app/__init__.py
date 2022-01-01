from flask import Flask, Blueprint, request, session, render_template, redirect, g
import os, sqlite3, json, urllib
from db import init_db
from datetime import date
from shop import refresh_shop

today = date.today()

import auth, game, db, shop


def create_app():
    app = Flask(__name__)
    # Configure app key & DB location
    app.config.from_mapping(
        SECRET_KEY = os.urandom(32),
        DATABASE = os.path.join(app.instance_path, db.DB_FILE)
    )

    # Ensure the DB location exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app

app = create_app()

# Connect Authentication Blueprint
app.register_blueprint(auth.bp)

# Connect Game Blueprint
app.register_blueprint(game.bp)

with app.app_context():
    init_db()
    d = db.get_db()
    c = d.cursor()

# Homepage render function
@app.route("/", methods=['GET', 'POST'])
def home():
    if auth.is_logged_in():
        return render_template("home.html")
    else:
        return auth.login()

@app.route("/profile", methods=['GET', 'POST'])
@auth.login_required
def profile():
    d = db.get_db()
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
        itemList = item.split(",")
        if itemList[0] == "card_color":
            colors.append(itemList[2])
        if itemList[0] == "pfp":
            pfps.append(itemList[2])
    return render_template("profile.html",username=session['username'],balance=balance,wins=wins,picture_list=pfps,color_list=colors,current_color=currColor)

@app.route("/shop", methods=['GET', 'POST'])
@auth.login_required
def shop():
    if request.method == 'POST':
        d = db.get_db()
        c = d.cursor()

        purchasedItem = request.form['itemName']
        print(purchasedItem)
        c.execute("SELECT * FROM USERS WHERE USERNAME = (?)", (session['username'],))
        userPoints = c.fetchone()
        c.execute("SELECT * FROM SHOP WHERE NAME = (?)", (purchasedItem,))
        itemData = c.fetchone()
        print(itemData)
        #check and subtract points
        if userPoints[2] < itemData[3]:
            return render_template("shop.html",error="You're broke")
        c.execute("UPDATE USERS SET POINTS = (?) WHERE USERNAME = (?)", (userPoints[2]-itemData[3], session['username']))
        #remove item from market
        c.execute("DELETE FROM SHOP WHERE NAME = (?)", (purchasedItem,))
        #update inventory
        d.commit()
        inventory_path = "inventories/%s.txt" % session['username']
        with open(inventory_path, "a") as inventory:
            inventory.write(""+itemData[0]+"/"+itemData[1]+"/"+itemData[2])
            inventory.write("\n")



    refresh_shop()
    d = db.get_db()
    c = d.cursor()
    c.execute("SELECT * FROM SHOP")
    items = c.fetchall()
    c.execute("SELECT * FROM USERS WHERE USERNAME = (?)", (session['username'],))
    userPoints = c.fetchone()
    return render_template("shop.html",items=items,balance=userPoints[2])



if __name__ == "__main__":
    app.debug = True
    app.run()
