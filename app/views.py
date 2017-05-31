from app import app
from app import scraper
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')
