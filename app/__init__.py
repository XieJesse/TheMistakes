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

@app.route("/play",methods=['GET', 'POST'])
@auth.login_required
def play():
    return render_template("setup.html")

# Homepage render function
@app.route("/", methods=['GET', 'POST'])
def home():
    if auth.is_logged_in():
        return render_template("home.html")
    else:
        return auth.login()

@app.route("/shop", methods=['GET', 'POST'])
@auth.login_required
def shop():
    if auth.is_logged_in():

        if request.method == 'POST':
            d = db.get_db()
            c = d.cursor()

            purchasedItem = request.form['itemName']
            print(purchasedItem)
            c.execute("SELECT * FROM USERS WHERE USERNAME = (?)", (session['username'],))
            userPoints = c.fetchone()
            c.execute("SELECT * FROM SHOP WHERE RGB_URL = (?)", (purchasedItem,))
            itemData = c.fetchone()
            print(itemData)
            #check and subtract points
            if userPoints[2] < itemData[3]:
                return render_template("shop.html",error="You're broke")
            c.execute("UPDATE USERS SET POINTS = (?) WHERE USERNAME = (?)", (userPoints[2]-itemData[3], session['username']))
            #remove item from market
            c.execute("DELETE FROM SHOP WHERE RGB_URL = (?)", (purchasedItem,))
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
    else:
        return auth.login()



if __name__ == "__main__":
    app.debug = True
    app.run()
