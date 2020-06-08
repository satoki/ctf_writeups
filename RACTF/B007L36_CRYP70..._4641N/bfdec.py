import binascii
import socket
import re

#c = "w4bDkMKDw6jDi8Ouw6JQw6jDh8OZwojCmMONw4nDnsKtwqnDk8OiwqLDosKdw6XDhsOVw6rDj8Oew5NcwpTDhMOiw4vCpcOYw5bDoFTCrcOHw6LCpsKUw6PDm8ONw4jClMOdw6TDosKYwpTDmMOjw53CpX/DicObwqHCqcOAw6fCrMKUw6bDpcOUw5jDmcOKwpvDocKVw5fDkcOZw5xTw4rDi8OlVMKaw43DnVPDmcOrw6XDlsOVw5nChsOvw5bCkcOof8Odw5xTw5HDi8OfwqnCpcOTw6xTw53Dq8KSw5XDi8OZwobDnsOXwqDDnMOEw6bDnMKYw5fDmsKawqjCscOTwpnCmcOdw6nDl8KP"
#p = "To test the encryption service, encrypt this file with your company issued secret key and ensure that it results in the ciphertext.txt file."
c = "w6TDgsOGw6jDjMO2w5RgwqTDi8OTw5Vmwr7CncOjZcKcwpLDmGjDnMKxw5/ClMOCwqTDlMOaw5tjw7E="
p = "ractf{n0t_th3_fl49_y3t}ractf{n0t_th3_fl49_y3t}ractf{n0t_th3_fl49_y3t}ractf{n0t_th3_fl49_y3t}ractf{n0t_th3_fl49_y3t}"

now = "ractf{"
flag = 0
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('95.216.233.106', 10930))
while True:
    for i in "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ_{} ":
        s.sendall(p.encode("utf-8")+b"\n")
        _ = s.recv(1024)
        s.sendall(now.encode("utf-8")+i.encode("utf-8")+b"\n")
        data = s.recv(1024)
        a = re.search(".*: (?P<base64>.*)\S\S\S\SPlease", str(data))
        a = a.group("base64")
        print("Cry:"+c)
        print("Now:"+a)
        if (binascii.a2b_base64(c).decode("utf-8")).startswith(binascii.a2b_base64(a).decode("utf-8")):
            now += i
            print("Cry:"+c)
            print("Hit:"+a)
            print()
            print("********************"+now+"********************")
            print()
            flag = 1
            break
    if flag==0:
        print("Error")
        break