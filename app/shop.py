from flask import Flask, Blueprint, request, session, render_template, redirect, g
import os, sqlite3, json, urllib
from datetime import date
from app import auth
import random
from app.db import get_db
bp = Blueprint('shop', __name__)

today = date.today()

@bp.route("/shop", methods=['GET', 'POST'])
@auth.login_required
def shop():
    try:
        #if item is bought
        if request.method == 'POST':
            d = get_db()
            c = d.cursor()

            purchasedItem = request.form['itemName']
            # print(purchasedItem)
            c.execute("SELECT * FROM USERS WHERE USERNAME = (?)", (session['username'],))
            userData = c.fetchone()
            c.execute("SELECT * FROM SHOP WHERE NAME = (?)", (purchasedItem,))
            itemData = c.fetchone()
            c.execute("SELECT * FROM SHOP")
            items = c.fetchall()
            # print(itemData)
            #check and subtract points
            if userData[2] < itemData[3]:
                return render_template("shop.html",error="You're broke", balance = userData[2], items=items)
            c.execute("UPDATE USERS SET POINTS = (?) WHERE USERNAME = (?)", (userData[2]-itemData[3], session['username']))
            #remove item from market
            c.execute("DELETE FROM SHOP WHERE NAME = (?)", (purchasedItem,))
            # set pfp to default if it is the only one
            if userData[4] == "https://media.istockphoto.com/vectors/messenger-profile-icon-on-white-isolated-background-vector-vector-id1316947194?b=1&k=20&m=1316947194&s=170667a&w=0&h=m1EuwYY4Z0R4X33z8rmQzLW2r_yx9SWVotY-wPfcA9s=" and itemData[0] == "pfp":
                c.execute("UPDATE USERS SET PROFILE_PICTURE = (?) WHERE USERNAME = (?)", (itemData[2],session['username']))
                #rewrite inventory so that pfp is first
                inventory_path = "inventories/%s.txt" % session['username']
                with open(inventory_path, "r+") as inventory:
                    allItems = inventory.readlines()
                    index = 0
                    for line in allItems:
                        lineList = line.split("|")
                        if lineList[2].strip() == itemData[2].strip():
                            index = len(line)
                            inventory.seek(0)
                            inventory.write(line)
                    inventory.seek(index)
                    for line in allItems:
                        lineList = line.split("|")
                        if lineList[2].strip() != itemData[2].strip():
                            inventory.write(line)

            d.commit()
            #update inventory
            inventory_path = "inventories/%s.txt" % session['username']
            with open(inventory_path, "a") as inventory:
                inventory.write(""+itemData[0]+"|"+itemData[1]+"|"+itemData[2])
                inventory.write("\n")
            #run refresh_shop method
        refresh_shop()
        d = get_db()
        c = d.cursor()
        c.execute("SELECT * FROM SHOP")
        items = c.fetchall()
        c.execute("SELECT * FROM USERS WHERE USERNAME = (?)", (session['username'],))
        userData = c.fetchone()
        #render shop.html with parameters
        return render_template("shop.html",items=items,balance=userData[2])
    except:
        return render_template("login.html", error ="An error has occurred with the shop")


def refresh_shop():

    d = get_db()
    c = d.cursor()

    c.execute("SELECT * FROM SHOP")
    existing_item = c.fetchone()
    if not existing_item:
        # add if table is empty
        for i in range(0,3):
            randColor = randomColor()
            if randColor[0] == "error":
                c.execute("SELECT * FROM USERS WHERE USERNAME = (?)", (session['username'],))
                userData = c.fetchone()
                return render_template("shop.html",error="There was an error with the Color API",balance=userData[2])
            # will generate random color based on day
            itemInfo = ["card_color",randColor[0],randColor[1],random.randint(100,250),today.strftime("%m/%d/%y")]
            # print(itemInfo)
            addItem = "INSERT INTO SHOP VALUES(?,?,?,?,?)"
            c.execute(addItem,itemInfo)

            randPFP = randomPFP()
            if randPFP[0] == "error":
                c.execute("SELECT * FROM USERS WHERE USERNAME = (?)", (session['username'],))
                userData = c.fetchone()
                return render_template("shop.html",error="There was an error with the Lorem Picsum API",balance=userData[2])
            # will generate random pfp based on day
            itemInfo = ["pfp",randPFP[0],randPFP[1],random.randint(100,250),today.strftime("%m/%d/%y")]
            # print(itemInfo)
            addItem = "INSERT INTO SHOP VALUES(?,?,?,?,?)"
            c.execute(addItem,itemInfo)
            d.commit()

    if existing_item:
        if existing_item[4] != today.strftime("%m/%d/%y"):
            # clear table and add if date does not match (table stays the same if date matches)
            c.execute("DELETE FROM SHOP")

            for i in range(0,2):
                randColor = randomColor()
                if randColor[0] == "error":
                    c.execute("SELECT * FROM USERS WHERE USERNAME = (?)", (session['username'],))
                    userData = c.fetchone()
                    return render_template("shop.html",error="There was an error with the Color API",balance=userData[2])
                #will generate random color based on day
                itemInfo = ["card_color",randColor[0],randColor[1],random.randint(100,300),today.strftime("%m/%d/%y")]
                # print(itemInfo)
                addItem = "INSERT INTO SHOP VALUES(?,?,?,?,?)"
                c.execute(addItem,itemInfo)

                randPFP = randomPFP()
                if randPFP[0] == "error":
                    c.execute("SELECT * FROM USERS WHERE USERNAME = (?)", (session['username'],))
                    userData = c.fetchone()
                    return render_template("shop.html",error="There was an error with the Lorem Picsum API",balance=userData[2])
                # will generate random pfp based on day
                itemInfo = ["pfp",randPFP[0],randPFP[1],random.randint(100,250),today.strftime("%m/%d/%y")]
                # print(itemInfo)
                addItem = "INSERT INTO SHOP VALUES(?,?,?,?,?)"
                c.execute(addItem,itemInfo)
                d.commit()

def randomColor():
    try:
        hexList = "0123456789ABCDEF"
        randomColor = hexList[random.randint(0,15)]+hexList[random.randint(0,15)]+hexList[random.randint(0,15)]+hexList[random.randint(0,15)]+hexList[random.randint(0,15)]+hexList[random.randint(0,15)]
        # opens up API data (API data being a randomly generated color hex value)
        req = urllib.request.Request('https://www.thecolorapi.com/id?hex='+randomColor, headers={'User-Agent': 'Mozilla/5.0'}) #change deck count for more decks of 52
        data = urllib.request.urlopen(req)
        # reads API data into variable (comes in as JSON data)
        response = data.read()
        # converts JSON data to python dictionary
        response_info = json.loads(response)
        # sets a variable dictionary with color data
        color = response_info["name"]
        RGB = response_info["rgb"]
        # set variable for rgb values
        colorName = color['value']
        # set variable for color name
        colorRGB = str(RGB["r"])+","+str(RGB["g"])+","+str(RGB["b"])
        return [colorName,colorRGB]
    except:
        return ["error","error"]

def randomPFP():
    try:
        # opens up API data (API data being a randomly generated image from api)
        req = urllib.request.Request('https://picsum.photos/v2/list?limit=1&page='+str(random.randint(0,993)), headers={'User-Agent': 'Mozilla/5.0'})
        data = urllib.request.urlopen(req)
        # reads API data into variable (comes in as JSON data)
        response = data.read()
        # converts JSON data to python dictionary
        response_info = json.loads(response)
        name = "Image "+str(response_info[0]["id"])
        # set variable for image "name"
        url = response_info[0]["download_url"]
        # set variable for image url
        return [name,url]
    except:
        return ["error","error"]
