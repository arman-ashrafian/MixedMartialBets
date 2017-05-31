from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
import os
import schedule
from threading import Thread
import datetime
import time

app = Flask(__name__, static_url_path='/static')

base_dir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'database.sqlite3')
app.secret_key = 'supersecretkey'
db = SQLAlchemy(app)

from app import views, models, scraper

def updateDatabase():
    fights = scraper.getFights()

    today = datetime.datetime.now()

    # This will break in 983 years
    fightDate = datetime.datetime.strptime(fights[0].date[0:-1], '%m-%d-%Y')


    if(today <= fightDate):
        for fight in fights:
            fightQuery = models.Fight.query.filter_by(fighterA=fight.fighterA).first()
            if(fight.oddA != fightQuery.oddA):
                fightQuery.oddA = fight.oddA
            if(fight.oddB != fightQuery.oddB):
                fightQuery.oddB = fight.oddB
            print("Updated the Database")

    else:
        try:
            for fight in fights:
                db.session.add(fight)
        except:
            print("Error Adding to Database")

    db.session.commit()




# Runs on background thread
def runBackgroundThread():
    while True:
        schedule.run_pending()

# Update database background task set up
def scheduleTask():
    # update database every 10 seconds
    schedule.every(30).minutes.do(updateDatabase)

    t = Thread(target=runBackgroundThread)
    t.start()
    print("Starting Background Tasks")

scheduleTask()
