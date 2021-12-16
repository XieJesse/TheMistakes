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
            # will generate random color based on day
            itemInfo = ["card_color","#105e91","",random.randint(100,300),today.strftime("%m/%d/%y")]
            addItem = "INSERT INTO SHOP VALUES(?,?,?,?,?)"
            c.execute(addItem,itemInfo)
            d.commit()

    if existing_item:
        if existing_item[4] != today.strftime("%m/%d/%y"):
            # clear table and add if date does not match (table stays the same if date matches)
            c.execute("DROP * FROM SHOP")

            for i in range(0,2):
                #will generate random color based on day
                itemInfo = ["card_color","#105e91","",random.randint(100,300),today.strftime("%m/%d/%y")]
                addItem = "INSERT INTO SHOP VALUES(?,?,?,?,?)"
                c.execute(addItem,itemInfo)
                d.commit()
