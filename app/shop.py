from flask import Flask, Blueprint, request, session, render_template, redirect, g
import os, sqlite3, json, urllib
from datetime import date
import random
from db import get_db

today = date.today()

def refresh_shop():

    d = get_db()
    c = d.cursor()

    c.execute("SELECT * FROM SHOP")
    existing_item = c.fetchone()
    if not existing_item:
        # add if table is empty
        for i in range(0,2):
            color = randomColor()
            # will generate random color based on day
            itemInfo = ["card_color",color[0],color[1],"",random.randint(100,300),today.strftime("%m/%d/%y")]
            print(itemInfo)
            addItem = "INSERT INTO SHOP VALUES(?,?,?,?,?,?)"
            c.execute(addItem,itemInfo)
            d.commit()

    if existing_item:
        if existing_item[4] != today.strftime("%m/%d/%y"):
            # clear table and add if date does not match (table stays the same if date matches)
            c.execute("DROP * FROM SHOP")

            for i in range(0,2):
                #will generate random color based on day
                itemInfo = ["card_color",color[0],color[1],"",random.randint(100,300),today.strftime("%m/%d/%y")]
                print(itemInfo)
                addItem = "INSERT INTO SHOP VALUES(?,?,?,?,?,?)"
                c.execute(addItem,itemInfo)
                d.commit()

def randomColor():
    hexList = "0123456789ABCDEF"
    randomColor = hexList[random.randint(0,15)]+hexList[random.randint(0,15)]+hexList[random.randint(0,15)]+hexList[random.randint(0,15)]+hexList[random.randint(0,15)]+hexList[random.randint(0,15)]
    # opens up API data (API data being a randomly made deck)
    req = urllib.request.Request('https://www.thecolorapi.com/id?hex='+randomColor, headers={'User-Agent': 'Mozilla/5.0'}) #change deck count for more decks of 52
    data = urllib.request.urlopen(req)
    # reads API data into variable (comes in as JSON data)
    response = data.read()
    # converts JSON data to python dictionary
    response_info = json.loads(response)
    # sets a variable deckid equal to the deck_id of the drawn deck
    color = response_info["name"]
    HSL = response_info["hsl"]
    colorName = color['value']
    colorHSL = HSL["h"]+"/"+HSL["s"]+"/"+HSL["l"]
    return [colorName,colorHSL]
