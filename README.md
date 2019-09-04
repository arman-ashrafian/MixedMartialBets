# MixedMartialBets

This web app lets user place mock bets on upcoming MMA fights. The application relies on web scraping to get betting
odds. The backend is created using Flask and the frontend is created using MaterializeCSS and
vanilla JavaScript. 


### Project Structure

* `run.py` - use this script to start the web server (`python3 run.py`)
* `addResults.py` - this script is used to add fight results to the database and also calculates the user winnings
* `scraper.py` - this script uses the beautifulsoup4 libarary to scrape www.bestfightodds.com/ and populates the 
database with the betting odds for upcoming fights
* `app/`
  * `__init__.py` - configures flask application and sqlite database
  * `models.py` - contains the models for the 3 database tables
  * `views.py` - contains the logic "business logic" for each route 
  * `templates/` - frontend of the application
  

### Screenshots

#### home 
![home](https://github.com/arman-ashrafian/MixedMartialBets/blob/master/screenshots/home_page.png)
#### place bets
![place bets](https://github.com/arman-ashrafian/MixedMartialBets/blob/master/screenshots/place_bets.png)
#### profile
![profile](https://github.com/arman-ashrafian/MixedMartialBets/blob/master/screenshots/profile.png)


### Run Locally

* start venv
```
source ven/bin/activate
```
* create database
```
$ python3 
>>> from app import db
>>> db.create_all()
>>> db.session.commit()
```
* start web server
```
$ python3 run.py
```
