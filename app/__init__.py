# INIT
# - this file initializes the flask app and sets up the background task
#   to scrape the fight odds

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
from flask_admin import Admin
import os
import schedule
from threading import Thread
import datetime
import time

app = Flask(__name__)

base_dir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'database.sqlite3')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'supersecretkey'
db = SQLAlchemy(app)
admin = Admin(app)

from app import views, models, scraper

def updateDatabase():
    print("Running Database Update")

    fights = scraper.getFights()

    # RETURN if no fights were scraped
    if fights == None: return

    # get fights in database
    dbFights = models.Fight.query.all()

    for fight in fights:
        update = False
        for dbFight in dbFights:
            if fight.event == dbFight.event and fight.fighterA == dbFight.fighterA and fight.fighterB == dbFight.fighterB:
                # update fight odds
                dbFight.oddA = fight.oddA
                dbFight.oddB = fight.oddB
                print("Updated Odds")
                update = True
        if not update:
            # add new fight to db
            try:
                db.session.add(fight)
            except:
                print("Error adding to databse")
    db.session.commit()

# Runs on background thread
def runBackgroundThread():
    while True:
        schedule.run_pending()
        time.sleep(1)

# Database-update task set up
def scheduleTask():
    # update database every 10 seconds
    schedule.every(30).minutes.do(updateDatabase)

    t = Thread(target=runBackgroundThread)
    t.start()
    print("Starting Background Task")

scheduleTask() # -- starts background thread
