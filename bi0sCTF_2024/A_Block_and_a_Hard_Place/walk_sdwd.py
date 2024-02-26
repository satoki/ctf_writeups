from ptrlib import *

sock = Socket("nc 13.201.224.182 31470")

# sock.debug = True

# Init(↑)
KEY = "w"
while True:
    sock.sendlineafter("> ", KEY)
    res = sock.recvuntil("\n")
    if b"You can't move there!" in res:  # Wall or Out of range
        sock.sendlineafter("> ", KEY.upper())
        res = sock.recvuntil("\n")
        if b"You can't move there!" in res:  # Out of range
            break

# Init(←)
KEY = "a"
while True:
    sock.sendlineafter("> ", KEY)
    res = sock.recvuntil("\n")
    if b"You can't move there!" in res:  # Wall or Out of range
        sock.sendlineafter("> ", KEY.upper())
        res = sock.recvuntil("\n")
        if b"You can't move there!" in res:  # Out of range
            break

print("Init Done!")

maze_data = ""

count = 0
while True:
    line = "｜"
    while True:
        KEY = "s"  # ↓
        if count % 2:
            KEY = "w"  # ↑
        sock.sendlineafter("> ", KEY)
        res = sock.recvuntil("\n")
        now = "　"
        if b"You can't move there!" in res:  # Wall or Out of range
            sock.sendlineafter("> ", KEY.upper())
            res = sock.recvuntil("\n")
            now = "｜"
            if b"You can't move there!" in res:  # Out of range
                line += "｜"
                break
        line += now
    if count % 2:
        maze_data += f"{line[::-1]}\n"
    else:
        maze_data += f"{line}\n"
    KEY = "d"  # →
    sock.sendlineafter("> ", KEY)
    res = sock.recvuntil("\n")
    if b"You can't move there!" in res:  # Wall or Out of range
        sock.sendlineafter("> ", KEY.upper())
        res = sock.recvuntil("\n")
        if b"You can't move there!" in res:  # Out of range
            break
    count += 1

print(maze_data)
