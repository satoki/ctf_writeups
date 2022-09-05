import json
import requests

session = requests.Session()
session.get("http://misc.2022.cakectf.com:10011/user/new")
while True:
    res = session.get("http://misc.2022.cakectf.com:10011/game/new").text
    #print(f"player_hand: {json.loads(res)['player_hand']}")
    res = session.get("http://misc.2022.cakectf.com:10011/game/act", params={"action": "stand"}).text
    if "CakeCTF" in res:
        print(f"flag: {json.loads(res)['flag']}")
        break
    if "lose" in res:
        session.get("http://misc.2022.cakectf.com:10011/user/new")
    print(f"money: {json.loads(res)['money']}")