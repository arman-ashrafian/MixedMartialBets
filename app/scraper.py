import pandas as pd
import bs4 as bs
import urllib.request
from app import models
from datetime import datetime



def getFights():
    url = "http://www.foxsports.com/ufc/odds"
    try:
        dfs = pd.read_html(url) #reads the html tables into a list of dataframe objects
    except:
        return None

    sauce = urllib.request.urlopen(url).read()
    soup = bs.BeautifulSoup(sauce, 'lxml')

    eventName = soup.find_all("option", {"selected":"selected"})[0].text
    date = soup.find_all("span", {"class":"wisbb_fightDate"})[0].text

    # make fight-odd dictionary
    fight = dict()
    for x in range(0, len(dfs)):
        #fight contains the fighters and the odds
        fight[x] = dfs[x][['Fighters', 'Opening Moneyline', 'Current Moneyline']][0:1]

    fighters = []
    for n in range(0, len(dfs)):                        #creates a list of all the fighters in order
        s = fight[n]['Fighters'][0]
        x = 0
        names = s.split()
        fighter1 = names[0] + " " + names[1][0:-1]                  #fighter A
        fighter2 = names[2][len(names[1])-1:] + " " + names[4]      #fighter B
        fighters.append(fighter1)
        fighters.append(fighter2)

    odds2 = []                                           #creates a list of all the odds in order
    for x in range(0, len(dfs)):
        for i in range(0,2):
            if i == 0:
                odds2.append(fight[x]['Current Moneyline'][0][0:4])
            else:
                odds2.append(fight[x]['Current Moneyline'][0][4:])

    fightObjects = []

    for i in range(0,int(len(odds2)/2) + 1,2):

        dateSplit = date.split(',')
        year = dateSplit[2][1:6]
        datetime_obj = datetime.strptime(dateSplit[1][1:], '%b %d')
        date_final = "%d-%d-%s" % (datetime_obj.month, datetime_obj.day, year)


        fightObjects.append(models.Fight(eventName, date_final, fighters[i], odds2[i], fighters[i+1], odds2[i+1]))


    return fightObjects
