from flask import Flask, session, render_template, redirect
import sqlite3

app = Flask(__name__)



# Homepage render function
@app.route("/")
def hello_user():
    return "who ar you?"

if __name__ == "__main__":
    app.debug = True
    app.run()
