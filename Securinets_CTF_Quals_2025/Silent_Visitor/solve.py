from ptrlib import *

sock = Socket("nc foren-1f49f8dc.p1.securinets.tn 1337")

print(sock.recvuntil("Input: ").decode(), end="")
answer = "122b2b4bf1433341ba6e8fefd707379a98e6e9ca376340379ea42edb31a5dba2"
print("\033[91m" + answer + "\033[0m")
sock.sendline(answer)

print(sock.recvuntil("Input: ").decode(), end="")
answer = "19045"
print("\033[91m" + answer + "\033[0m")
sock.sendline(answer)

print(sock.recvuntil("Input: ").decode(), end="")
answer = "192.168.206.131"
print("\033[91m" + answer + "\033[0m")
sock.sendline(answer)

print(sock.recvuntil("Input: ").decode(), end="")
answer = "Thunderbird"
print("\033[91m" + answer + "\033[0m")
sock.sendline(answer)

print(sock.recvuntil("Input: ").decode(), end="")
answer = "ammar55221133@gmail.com"
print("\033[91m" + answer + "\033[0m")
sock.sendline(answer)

print(sock.recvuntil("Input: ").decode(), end="")
answer = "masmoudim522@gmail.com"
print("\033[91m" + answer + "\033[0m")
sock.sendline(answer)

print(sock.recvuntil("Input: ").decode(), end="")
answer = "https://tmpfiles.org/dl/23860773/sys.exe"
print("\033[91m" + answer + "\033[0m")
sock.sendline(answer)

print(sock.recvuntil("Input: ").decode(), end="")
answer = "be4f01b3d537b17c5ba7dc1bb7cd4078251364398565a0ca1e96982cff820b6d"
print("\033[91m" + answer + "\033[0m")
sock.sendline(answer)

print(sock.recvuntil("Input: ").decode(), end="")
answer = "40.113.161.85"
print("\033[91m" + answer + "\033[0m")
sock.sendline(answer)

print(sock.recvuntil("Input: ").decode(), end="")
answer = "5000"
print("\033[91m" + answer + "\033[0m")
sock.sendline(answer)

print(sock.recvuntil("Input: ").decode(), end="")
answer = "http://40.113.161.85:5000/helppppiscofebabe23"
print("\033[91m" + answer + "\033[0m")
sock.sendline(answer)

print(sock.recvuntil("Input: ").decode(), end="")
answer = "3649ba90-266f-48e1-960c-b908e1f28aef"
print("\033[91m" + answer + "\033[0m")
sock.sendline(answer)

print(sock.recvuntil("Input: ").decode(), end="")
answer = "HKEY_CURRENT_USER\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run\\MyApp"
print("\033[91m" + answer + "\033[0m")
sock.sendline(answer)

print(sock.recvuntil("Input: ").decode(), end="")
answer = "C:\\Users\\ammar\\Documents\\sys.exe"
print("\033[91m" + answer + "\033[0m")
sock.sendline(answer)

print(sock.recvuntil("Input: ").decode(), end="")
answer = "e7bcc0ba5fb1dc9cc09460baaa2a6986"
print("\033[91m" + answer + "\033[0m")
sock.sendline(answer)

sock.sh(prompt="")
