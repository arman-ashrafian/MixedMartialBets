from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
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

from app import views, models, scraper

def updateDatabase():
    print("Running Database Update")
    fights = scraper.getFights()

    # fights == None if no datafram in foxsports
    if fights != None:

        today = datetime.datetime.now()

        dbFights = models.Fight.query.all()

        fightDate = datetime.datetime.strptime(dbFights[len(dbFights)-1].date[0:-1], '%m-%d-%Y')


        if(today <= fightDate):
        # Update the current fights
            for fight in fights:
                fightQuery = models.Fight.query.filter(and_(models.Fight.fighterA == fight.fighterA,
                                                            models.Fight.fighterB == fight.fighterB)).first()
                if(fightQuery):
                    if(fight.oddA != fightQuery.oddA):
                        fightQuery.oddA = fight.oddA
                    if(fight.oddB != fightQuery.oddB):
                        fightQuery.oddB = fight.oddB
                    print("Updated the Database: " + str(fight))


        else:
        # add new fights to database
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
    schedule.every(1).minutes.do(updateDatabase)

    t = Thread(target=runBackgroundThread)
    t.start()
    print("Starting Background Task")

scheduleTask()
