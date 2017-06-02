from app import app
from app import scraper
from app import db
from app import models
from flask import render_template, request, session, redirect, url_for

@app.route('/')
@app.route('/index')
def index():
    if 'username' in session:
        currentUser = session['username']
        return render_template('index.html', logged_in=True, user_name=currentUser)

    return render_template('index.html', logged_in=False)

@app.route('/signup')
def signUp():
    return render_template('signUp.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
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

                db.session.add(newUser)
                db.session.commit()
                return redirect(url_for('index'))
            else:
                # email already exists
                return render_template("signUp.html", empty_form=False, emailError=True)
    return render_template("signUp.html")
