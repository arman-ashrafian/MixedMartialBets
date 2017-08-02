# VIEWS
# - routes and template rendering

from app import app
from app import db
from app import models
from app import admin
from flask import render_template, request, session, redirect, url_for, jsonify
from flask_admin.contrib.sqla import ModelView
from datetime import datetime

# AdminModelView
# - auth logic for admin page
# - obviously not very secure
class AdminModelView(ModelView):

    def is_accessible(self):
        try:
            return session['username'] == 'admin' and session['email'] == 'admin@admin.com'
        except KeyError:
            return False
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('index'))

# Admin Views
admin.add_view(AdminModelView(models.Fight, db.session))
admin.add_view(AdminModelView(models.User, db.session))
admin.add_view(AdminModelView(models.Bet, db.session))

@app.route('/')
@app.route('/index')
def index():
    currentUser = getCurrentUser()
    dbFights = models.Fight.query.all()
    fights = []

    # get newest event name WITH RESULTS
    for fight in dbFights:
        if fight.result != 0:
            eventName = fight.event

    # get latest fights WITH RESULTS
    for fight in dbFights:
        if(fight.event == eventName):
            fights.append(fight)

    loggedIn = currentUser != None #-- true if user is logged in

    return render_template('index.html', fights=fights, event_name=eventName,
                           logged_in=loggedIn, user_name=currentUser)

@app.route('/signup')
def signUp():
    currentUser = getCurrentUser()
    if currentUser:
        return render_template('signUp.html', logged_in=True, user_name=currentUser)
    return render_template('signUp.html', logged_in=False)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('email', None)
    return redirect(url_for('index'))

@app.route('/registerUser', methods=["POST", "GET"])
def registerUser():
    if request.method == "POST":

        # check if form is empty
        if not request.form['username'] or not request.form['email'] or not request.form['password']:
            return jsonify(status='bad', error='empty_form')

        elif not '@' in request.form['email']:
            return jsonify(status='bad', error='info', illegal_email='True')
        else:
            # check if email/username already exists in database
            emailQuery = models.User.query.filter_by(email=request.form['email']).first()
            nameQuery = models.User.query.filter_by(name=request.form['username']).first()

            if not emailQuery and not nameQuery:
                # add User to database
                newUser = models.User(request.form['username'], request.form['email'], request.form['password'], 1000)

                session['username'] = request.form['username']
                session['email'] = request.form['email']

                db.session.add(newUser)
                db.session.commit()

                return jsonify(status='ok')
            else:
                # email already exists
                emailErr = False
                nameErr = False
                if(emailQuery):
                    emailErr = True
                if(nameQuery):
                    nameErr = True
                return jsonify(status='bad', error='info', email=str(emailErr), name=str(nameErr))

    return jsonify(status="bad")


@app.route('/signInUser', methods=['POST', 'GET'])
def signInUser():
    if request.method == 'POST':
        # check if form is empty
        if not request.form['email'] or not request.form['password']:
            return render_template('login.html', incorrect_login=True)

        else:
            user = models.User.query.filter_by(email=request.form['email']).first()

            if user and user.password == request.form['password']:
                # correct email & password
                session['username'] = user.name
                session['email'] = request.form['email']

                return redirect(url_for('index'))

            else:
                # incorrect login
                return render_template('login.html', incorrect_login=True)

@app.route('/placebets/<int:event>')
def placeBets(event):
    user = getCurrentUser()
    loggedIn = user != None
    allFights = models.Fight.query.all()

    events = []
    for fight in allFights:
        if fight.result == 0 and not fight.event in events:
            events.append(fight.event)

    eventName = events[event-1]

    fights = []
    for fight in allFights:
        if fight.event == eventName:
            fights.append(fight)

    return render_template('placeBets.html', event_name=eventName,
                           fights=fights, user_name=user, logged_in=loggedIn,
                           other_events=events)



@app.route('/createBet/<int:fightID>', methods = ['POST'])
def createBet(fightID):
    '''
    - Add new Bet to the database
    - Error Checking:
    - IF User not logged in -> redirect to login
    '''
    if request.method == 'POST':
        user = getCurrentUser()

        # Check if logged in
        if not user:
            return jsonify(status="bad", error="login")
        else:
            usermodel = models.User.query.filter_by(email=session['email']).first()

            # Check Funds
            if int(request.form['betAmount']) > usermodel.balance:
                return jsonify(status="bad", error="balance",
                               balance=usermodel.balance)
            else:
                print("odd " + request.form['odd'])
                newBet = models.Bet(fightID=fightID,
                                    userID=usermodel.id,
                                    amount=int(request.form['betAmount']),
                                    fighter=request.form['fighter'],
                                    odd=int(request.form['odd']))
                usermodel.balance -= int(request.form['betAmount'])
                db.session.add(newBet)
                db.session.commit()
                print("New bet added to database")

                return jsonify(status="ok")

@app.route('/profile')
def profile():
    user = getCurrentUser()
    loggedIn = user != None;

    # redirect to login if !loggedIn
    if not loggedIn: return redirect(url_for('login'))

    else:
        # get user
        userQuery = models.User.query.filter_by(name=user).first()

        # get user's bets
        bets = models.Bet.query.filter_by(userID=userQuery.id)
        bets_completed = []
        fights_completed = []
        payouts = []

        # get the completed fights the user bet on
        for bet in bets:
            fight = models.Fight.query.filter_by(id=bet.fightID).first()
            if fight.result != 0:
                bets_completed.append(bet)
                fights_completed.append(fight)
                if fight.result == 1:
                    if bet.fighter == fight.fighterA:
                        payouts.append(calcPayout(fight.oddA, bet.amount))
                    else:
                        payouts.append(0)
                elif fight.result == 2:
                    if bet.fighter == fight.fighterB:
                        payouts.append(calcPayout(fight.oddB, bet.amount))
                    else:
                        payouts.append(0)

        # get pending bets & fights
        bets_pending = []
        fights_pending = []
        for bet in bets:
            fight = models.Fight.query.filter_by(id=bet.fightID).first()
            if fight.result == 0:
                bets_pending.append(bet)
                fights_pending.append(fight)

        accountBalance = userQuery.balance

        return render_template('profilePage.html', logged_in=loggedIn,
                               user_name=user, account_balance=accountBalance,
                               completed_bets=zip(bets_completed, fights_completed, payouts),
                               pending_bets=zip(bets_pending, fights_pending),
                               completed_length=len(bets_completed), pending_length=len(bets_pending))

def getCurrentUser():
    currentUser = None
    if 'username' in session:
        currentUser = session['username']
    return currentUser

def calcPayout(odd, bet):
    if odd < 0:
        return abs(bet * (100/odd))
    else:
        return abs(bet * (odd/100))
