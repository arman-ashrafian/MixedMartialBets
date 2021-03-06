# MODELS
# - contains the database models
# - Models: Fight, User, Bet

from app import db

class Fight(db.Model):

    # Fight Table
    # id | Event Name | Date | Fighter A | Odd A | Fighter B | Odd B

    id = db.Column(db.Integer, primary_key=True, unique=True)
    event = db.Column(db.String(1000))
    date = db.Column(db.String(50))
    fighterA = db.Column(db.String(100))
    oddA = db.Column(db.Integer)
    fighterB = db.Column(db.String(100))
    oddB = db.Column(db.Integer)
    result = db.Column(db.Integer, default=0)

    # Constructor
    def __init__(self, event, date, fighterA, oddA, fighterB, oddB):
        self.event = event
        self.date = date
        self.fighterA = fighterA
        self.oddA = oddA
        self.fighterB = fighterB
        self.oddB = oddB

    # print method
    def __repr__(self):
        return self.fighterA + " vs. " + self.fighterB

class User(db.Model):

    id = db.Column('id', db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    balance = db.Column(db.Float)
    bets = db.relationship('Bet', backref='user', lazy='dynamic')

    def __init__(self, name, email, password, balance):
        self.name = name
        self.email = email
        self.password = password
        self.balance = balance

    # print method
    def __repr__(self):
        return self.name + " - id: " + str(self.id)

class Bet(db.Model):

    id = db.Column('id', db.Integer, primary_key=True, unique=True)
    fightID = db.Column(db.Integer)
    userID = db.Column(db.Integer, db.ForeignKey('user.id'))
    fighter = db.Column(db.String(100))
    amount = db.Column(db.Float)
    odd = db.Column(db.Integer)

    def __init__(self, fightID, userID, amount, fighter, odd):
        self.fightID = fightID
        self.userID = userID
        self.amount = amount
        self.fighter = fighter
        self.odd = odd

    # print method
    def __repr__(self):
        return "id: " + str(self.id)
