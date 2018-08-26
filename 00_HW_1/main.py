from random import randint


episode_winnings = 0
while episode_winnings < 80:
    won = False
    bet_amount = 1
    while not won:
        res = play_black(bet_amount)
        won = res > 0
        if won:
            episode_winnings += bet_amount
        else:
            episode_winnings -= bet_amount
            bet_amount *= 2

def play_black(bet_amount):
    num = randint(1,38)
    print num
    if num <= 18:
        return bet_amount*2