from flask import Flask, Blueprint, request, session, render_template, redirect, g
import os, sqlite3, json, urllib
from db import init_db

import auth, game, db, shop, leaderboard, profile


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

# Connect leaderboard Blueprint
app.register_blueprint(leaderboard.bp)

# Connect profile Blueprint
app.register_blueprint(profile.bp)

with app.app_context():
    init_db()
    d = db.get_db()
    c = d.cursor()

# Homepage render function
@app.route("/", methods=['GET', 'POST'])
def home():
    if auth.is_logged_in():
        d = db.get_db()
        c = d.cursor()
        c.execute("SELECT * FROM USERS WHERE USERNAME = (?)", (session['username'],))
        userData = c.fetchone()
        username = userData[0]
        balance = userData[2]
        wins = userData[3]
        return render_template("home.html",wins=wins,balance=balance,username=username)
    else:
        return auth.login()


if __name__ == "__main__":
    app.debug = True
    app.run()
