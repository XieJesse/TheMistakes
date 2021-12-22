from flask import Flask, request, session, render_template, redirect
import sqlite3
import json
import urllib

app = Flask(__name__)

# Misc Render Function for testing templating
@app.route("/", methods=['GET', 'POST'])
def test():
    # test_colors = ["#000000", "#f5493d", "#318fe0", "#78a6ce"]
    # test_rgb = ["238,58,58", "28,28,28", "255,255,255", "78, 78, 245"]
    # return render_template("setup.html", colors=test_rgb)
    return render_template("game.html")

if __name__ == "__main__":
    app.debug = True
    app.run()
