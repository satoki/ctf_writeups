import re
import requests

href = ""
response = ""

try:
    while True:
        url = "https://finger-warmup.chals.damctf.xyz/" + href
        response = requests.get(url)
        nexthref = re.search("<a href=\"(?P<next>.*)\">", response.text)
        href = nexthref.group("next")
        print(href)
        print(response.text)
except:
    print(response.text)