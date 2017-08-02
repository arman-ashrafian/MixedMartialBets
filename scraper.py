# Scrape fight data from www.bestfightodds.com
import bs4 as bs
import urllib.request
from app import models, db

def getFights():
    url = "https://www.bestfightodds.com/"
    class URLopener(urllib.request.FancyURLopener):
        version = "Mozilla/5.0"

    opener = URLopener()
    res = opener.open(url).read()
    soup = bs.BeautifulSoup(res, 'lxml')

    div = soup.find_all('div', {'class':'table-header'})

    #Returns event and date
    x = 0
    events = []
    while x < len(div)-1:
        children = div[x].findChildren()
        fight = []
        for i in range(0,2):
            fight.append(children[i].text)
        events.append(fight)
        x += 1

    #Returns fighters in a nested list
    divtag = soup.find_all('div', {'class':'table-scroller'})
    fighters = []
    for i in range(len(div)-1):
        f = []
        for j in range(len(divtag[i].find_all('tr', {'class':['even', 'odd']}))):
            f.append(divtag[i].find_all('tr', {'class':['even', 'odd']})[j].find_all('th', {"scope":"row"})[0].text)
        fighters.append(f)

    #returns odds in a nested list
    odds = []
    for i in range(len(div)-1):
        o = []
        for j in range(len(divtag[i].find_all('tr', {'class':['even', 'odd']}))):
            if(len(divtag[i].find_all('tr', {'class':['even', 'odd']})[j].find_all('span', {"class":"tw"})[1].text) > 4):
                o.append(divtag[i].find_all('tr', {'class':['even', 'odd']})[j].find_all('span', {"class":"tw"})[1].text[0:-1])
            else:
                o.append(divtag[i].find_all('tr', {'class':['even', 'odd']})[j].find_all('span', {"class":"tw"})[1].text)
        odds.append(o)

    fightObjects = []
    # create fight objects
    for i in range(len(div)-1):
        for j in range(0, len(divtag[i].find_all('tr', {'class':['even', 'odd']})), 2):
            fightObjects.append(models.Fight(events[i][0], events[i][1], fighters[i][j],
                                             odds[i][j], fighters[i][j+1], odds[i][j+1]))

    return fightObjects

def updateDatabase(fights):
    print("Running Database Update")

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

if __name__ == '__main__':
    updateDatabase(getFights())