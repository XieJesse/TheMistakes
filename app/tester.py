from flask import Flask, request, session, render_template, redirect
import sqlite3
import json
import urllib

app = Flask(__name__)

# Misc Render Function for testing templating
@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template("register.html", error = "An error has occured")

if __name__ == "__main__":
    app.debug = True
    app.run()
