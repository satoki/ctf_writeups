import time
import json
import requests

plus_code = open("mail.txt").read().split("\n")

for i in plus_code:
    try:
        time.sleep(1)
        res = json.loads(requests.get(f"https://plus.codes/api?address={i}".replace("+", "%2B")).text)
        print(f'{res["plus_code"]["geometry"]["bounds"]["northeast"]["lat"]},{res["plus_code"]["geometry"]["bounds"]["northeast"]["lng"]}')
    except Exception as e:
        #print(e)
        pass