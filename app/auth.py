from flask import Flask, Blueprint, request, session, render_template, redirect, url_for, g
from functools import wraps
import os, sqlite3, json, urllib

from db import get_db

bp = Blueprint('auth', __name__)

def login_required(f):
    """Denotes a page where a user must be logged in to access it. Redirects
    to the home page if the user isn't logged in."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not 'username' in session.keys():
            return redirect("/")
        return f(*args, **kwargs)
    return decorated_function

def is_logged_in():
    return 'username' in session.keys()

@bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        d = get_db()
        c = d.cursor()

        # Check if username is in the database
        c.execute("SELECT * FROM USERS WHERE USERNAME = (?)", (username,))
        existing_username = c.fetchone()

        if not existing_username:
            return render_template("login.html", error = "The username does not exist.")

        # Check if password matches password of inputted user
        if existing_username[1] != password:
            return render_template("login.html", error = "The password is incorrect")

        session['username'] = username
        return redirect("/")
    else:
        return render_template("login.html")

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        repassword = request.form['re-password']

        d = get_db()
        c = d.cursor()

        # Check if the username / password is empty
        if not username or not password: # Strings can be converted to booleans (Empty Strings = False)
            return render_template("register.html", error = "Password / username must not be empty")

        # Check if there are any occurences of the username in the database already
        c.execute("SELECT * FROM USERS WHERE USERNAME = (?)", (username,))
        existing_username = c.fetchone()

        if existing_username:
             return render_template("register.html", error = "Username is already taken.")
        if not username.isalnum():
            return render_template("register.html", error = "Username can only contain numbers and letters")
        if not password.isalnum():
            return render_template("register.html", error = "Password can only contain numbers and letters")
        if password != repassword:
            return render_template("register.html", error = "Password and re-entered password do not match")

        # Add user to database
        inventory_file = f"{username}.txt"
        inventory_dir = "inventories"

        # Join the inventory filename to the inventories path
        inventory_path = os.path.join(inventory_dir, inventory_file)

        # Ensure the directory exists before the file is made
        if not os.path.exists(inventory_dir):
            os.mkdir(inventory_dir)

        with open(inventory_path, "w") as inventory:
            inventory.write("card_color|black|0,0,0")
            inventory.write("\n")
            inventory.write("profile_background|white|0,0,100")
            inventory.write("\n")

        userInfo = [username,password,10000,0,0,"","#000000","#FFFFFF", inventory_file]
        c.execute("INSERT INTO USERS VALUES(?,?,?,?,?,?,?,?,?)", userInfo)
        d.commit()

        session['username'] = username
        return redirect("/")
    else:
        return render_template("register.html")

@bp.route("/logout", methods=['GET', 'POST'])
def logout():
    if request.method == 'GET':
        if is_logged_in():
            session.pop('username')
        return redirect("/")
    else:
        return redirect("/")
