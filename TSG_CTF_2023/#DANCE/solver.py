import requests

url = "http://34.84.176.251:8080/mypage.php"

for i in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789":
    for j in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789":
        try:
            # L%2B8C6ZQ%3D = base64enc(base64dec("Kf4K844%3D") ^ "guest" ^ "admin")
            res = requests.get(url, cookies={"auth": "L%2B8C6ZQ%3D", "iv": "AOF7azAiRHDSmEhE", "tag": f"{i}{j}"})
        except:
            print("Error")
            continue
        if "I know you rewrote cookies!" not in res.text:
                print(f"Found: {i}{j}")
                print(res.text)
                exit()