# Add result
# Run this script to add fight results
# User balances will be updated with winnings

from app import models
from app import db
from sqlalchemy import and_

def main():
    # get all pending fights
    fights = models.Fight.query.filter_by(result=0)

    # get the pending events
    events = []
    latestEvent = ""
    for fight in fights:
        if fight.event != latestEvent:
            events.append(fight.event)
            latestEvent = fight.event

    # display pending events
    i = 1
    for ev in events:
        print("%d. %s" % (i, ev))
        i += 1

    # user's choice for event
    eventChoice = int(input("Which event do you have result for? "))
    print()

    # query fights pending fights for that event
    fights = models.Fight.query.filter_by(event=events[eventChoice-1], result=0)

    # adding fight results to database
    bets = [] # -- uset bets for each fight
    fightList = [] # -- fights that have been updated
    for fight in fights:
        result = int(input("Result for %s: " % fight))
        fight.result = result

        for b in models.Bet.query.filter_by(fightID=fight.id):
            bets.append(b)

        fightList.append(fight)
        db.session.add(fight)

    db.session.commit()
    print()

    # add payout to user accounts
    for fight in fightList:
        for bet in bets:
            if bet.fightID == fight.id:
                pay = 0

                if fight.result == 1 and bet.fighter == fight.fighterA:
                    pay = bet.amount + calcPayout(fight.oddA, bet.amount)
                elif fight.result == 2 and bet.fighter == fight.fighterB:
                    pay = bet.amount + calcPayout(fight.oddB, bet.amount)

                user = models.User.query.filter_by(id=bet.userID).first()
                user.balance += pay
                print("User %d +$%.2f" % (user.id, pay))
                db.session.add(user)

    db.session.commit()


def calcPayout(odd, bet):
    if odd < 0:
        return abs(bet * (100/odd))
    else:
        return abs(bet * (odd/100))

if __name__ == '__main__':
    main()
