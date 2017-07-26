from app import models
from app import db
from sqlalchemy import and_

def main():
    fights = models.Fight.query.filter_by(result=0)

    events = []
    latestEvent = ""
    for fight in fights:
        if fight.event != latestEvent:
            events.append(fight.event)
            latestEvent = fight.event

    i = 1
    for ev in events:
        print("%d. %s" % (i, ev))

    eventChoice = int(input("Which event do you have result for? "))

    fights = models.Fight.query.filter_by(event=fight.event, result=0)

    bets = []
    results = []
    fightList = []
    for fight in fights:
        result = input("Result for %s: " % fight)
        results.append(result)
        fight.result = result
        bets.append(models.Bet.query.filter_by(fightID=fight.id).first())
        fightList.append(fight)
        db.session.add(fight)

    db.session.commit()


    for fight in fightList:
        for bet in bets:
            if not bet: break
            pay = 0
            if fight.result == 1 and bet.fighter == fight.fighterA:
                pay = bet.amount + calcPayout(fight.oddA, bet.amount)
            elif fight.result == 2 and bet.fighter == fight.fighterB:
                pay = bet.amount + calcPayout(fight.oddB, bet.amount)

            user = models.User.query.filter_by(id=bet.userID).first()
            user.balance += pay
            db.session.add(user)

    db.session.commit()


def calcPayout(odd, bet):
    if odd < 0:
        return abs(bet * (100/odd))
    else:
        return abs(bet * (odd/100))

if __name__ == '__main__':
    main()
