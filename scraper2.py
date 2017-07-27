import bs4 as bs
import urllib.request

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
#print(fighters)

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
#print(odds)

#This is how they would be added to each fight object
for i in range(len(div)-1):
    for j in range(0, len(divtag[i].find_all('tr', {'class':['even', 'odd']})), 2):
        print(events[i][0], events[i][1], fighters[i][j], odds[i][j], fighters[i][j+1], odds[i][j+1])
              #event name,   event date,    fighterA,      , oddA      , fighterB     ,   oddB

#prints fighters names line by line
# odds = []
# for tag in divtag:
#     name = tag.find_all('tr', {'class':['even', 'odd']})
#     for n in name:
#         llamo = n.find_all('span', {"class":"tw"})
#         for x in range(1,2):
#             odds.append
#             print(llamo[x].text)

#prints of the fighters in event x
#print(len(divtag[x].find_all('tr', {'class':['even', 'odd']})))
