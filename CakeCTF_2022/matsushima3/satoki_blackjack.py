import sys
import json
import time
import random
import requests


# by app.py
def calculate_score(cards):
    """Calculate current total of cards"""
    num_ace = 0
    score = 0
    for _, c in cards:
        if c == 0: num_ace += 1
        elif c < 10: score += c + 1
        else: score += 10

    while num_ace > 0:
        if 21 - score >= 10 + num_ace: score += 11
        else: score += 1
        num_ace -= 1

    return -1 if score > 21 else score


def future_prediction(user_id, player_hand):
    now_t = int(time.time())
    for i in range(now_t - 10, now_t + 10):
        deck = [[j // 13, j % 13] for j in range(4*13)]
        random.seed(i ^ user_id)
        random.shuffle(deck)
        if (player_hand[0] == deck[-1]) and (player_hand[1] == deck[-3]):
            return deck
    return []


session = requests.Session()
r = session.get("http://misc.2022.cakectf.com:10011/user/new")
user_id = json.loads(r.content)["user_id"]

while True:
    r = session.get("http://misc.2022.cakectf.com:10011/game/new")
    #print(r.content) #Debug
    player_hand = json.loads(r.content)["player_hand"]
    deck = future_prediction(user_id, player_hand)
    dealer_hand = [deck[-2], deck[-4]]
    deck = deck[:-4]

    player_score = calculate_score(player_hand)
    dealer_score = calculate_score(dealer_hand)

    #print("+----------New----------+")
    #print(deck)
    #print(f"PlayerHand:{player_hand} [{player_score}]")
    #print(f"DealerHand:{dealer_hand} [{dealer_score}]")

    for i in range(len(deck)):
        if calculate_score(player_hand + deck[-i:]) != -1:
            r = session.get("http://misc.2022.cakectf.com:10011/game/act", params={"action": "hit"})
            #print(r.content) #Debug
            if b"CakeCTF" in r.content: 
                print(json.loads(r.content.decode())["flag"])
                sys.exit()
            if (b"win" in r.content) or (b"draw" in r.content):
                break
            if b"lose" in r.content:
                session = requests.Session()
                r = session.get("http://misc.2022.cakectf.com:10011/user/new")
                user_id = json.loads(r.content)["user_id"]
                break
    else:
        r = session.get("http://misc.2022.cakectf.com:10011/game/act", params={"action": "stand"})
        #print(r.content) #Debug
        if b"lose" in r.content:
            session = requests.Session()
            r = session.get("http://misc.2022.cakectf.com:10011/user/new")
            user_id = json.loads(r.content)["user_id"]