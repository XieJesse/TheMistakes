from flask import Flask, Blueprint, request, session, render_template, redirect, g
import os, sqlite3, json, urllib
from db import init_db

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

# Connect Game Blueprint
app.register_blueprint(shop.bp)

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


if __name__ == "__main__":
    app.debug = True
    app.run()
