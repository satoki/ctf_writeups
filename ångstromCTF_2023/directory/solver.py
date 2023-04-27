import sys
import requests

i = 0
while i < 5000:
    try:
        print(i)
        res = requests.get(f"https://directory.web.actf.co/{i}.html").text
        if "your flag is in another file" != res:
            print(res)
            sys.exit(0)
        i += 1
    except Exception as e:
        print(e)
        continue