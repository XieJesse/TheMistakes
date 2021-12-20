from flask import Flask, Blueprint, request, session, render_template, redirect, g
import os, sqlite3, json, urllib

from db import get_db

bp = Blueprint('auth', __name__)

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
        repassword = request.form['repassword']

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
        if password == repassword:
            return render_template("register.html", error = "Password and re-entered password are already taken")

        # Add user to database
        userInfo = [username,password,0,0,0,"","#000000","#FFFFFF",username+".txt"]
        c.execute("INSERT INTO USERS VALUES(?,?,?,?,?,?,?,?,?)", userInfo)
        d.commit()

        inventory_path = "inventories/%s.txt" % username
        with open(inventory_path, "w") as inventory:
            inventory.write("card_color,black,0/0/0")
            inventory.write("\n")
            inventory.write("profile_background,white,0/0/100")
            inventory.write("\n")

        session['username'] = username
        return redirect("/")
    else:
        return render_template("register.html")
