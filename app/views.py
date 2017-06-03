from app import app
from app import scraper
from app import db
from app import models
from flask import render_template, request, session, redirect, url_for

@app.route('/')
@app.route('/index')
def index():
    currentUser = getCurrentUser()
    fights = models.Fight.query.all()
    eventName = fights[0].event;
    if currentUser:
        return render_template('index.html', logged_in=True,
                               user_name=currentUser, fights=fights,
                               event_name=eventName)
    return render_template('index.html', logged_in=False, fights=fights, event_name=eventName)

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
        if not request.form['name'] or not request.form['email'] or not request.form['password']:
            return render_template("signUp.html", empty_form=True, emailError=True)

        else:
            # check if email already exists in database
            if not models.User.query.filter_by(email=request.form['email']).first():
                # add User to database
                newUser = models.User(request.form['name'], request.form['email'], request.form['password'], 0)

                session['username'] = request.form['name']
                session['email'] = request.form['email']

                db.session.add(newUser)
                db.session.commit()
                return redirect(url_for('index'))
            else:
                # email already exists
                return render_template("signUp.html", empty_form=False, emailError=True)
    return render_template("signUp.html")


@app.route('/signInUser', methods=['POST', 'GET'])
def signInUser():
    if request.method == 'POST':
        # check if form is empty
        if not request.form['email'] or not request.form['password']:
            return render_template('login.html', incorrect_login=True)

        else:
            user = models.User.query.filter_by(email=request.form['email']).first()

            if user and user.password == request.form['password']:
                session['username'] = user.name
                session['email'] = request.form['email']

                return redirect(url_for('index'))

            else:
                return render_template('login.html', incorrect_login=True)

def getCurrentUser():
    currentUser = None
    if 'username' in session:
        currentUser = session['username']
    return currentUser
