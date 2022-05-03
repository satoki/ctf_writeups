import requests

url = "https://crumbs.web.actf.co/"
path = ""

while True:
    res = requests.get(url + path)
    text = res.text
    print(text)
    if "actf{" in text:
        break
    path = text.replace("Go to ", "")