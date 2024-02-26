from ptrlib import *
from time import time

logger.level = 0


# by kanon @_k4non
def solve_pow(s, debug=False):
    start = time()
    g = int(s.split("^")[0])
    p = int(s.split("mod ")[1].split(" == ")[0])
    target = int(s.split(" == ")[1])
    i = 0
    while True:
        if pow(g, i, p) == target:
            if debug:
                print(f"Time taken: {time()-start}")
            return i
        i += 1


sock = Socket("nc 13.201.224.182 30008")

PoW = sock.recvuntil("\n")
sock.sendlineafter("x: ", solve_pow(PoW.decode()))

# Q1
print(sock.recvuntil("}\n\n").decode())
sock.sendlineafter("Answer: ", "verboten{4C530001090312109353&0:2024-02-16-12-01-57}")

# Q2
print(sock.recvuntil("}\n\n").decode())
sock.sendlineafter("Answer: ", "verboten{11ecc1766b893aa2835f5e185147d1d2}")

# Q3
print(sock.recvuntil("}\n\n").decode())
sock.sendlineafter("Answer: ", "verboten{169cbd05b7095f4dc9530f35a6980a79}")

# Q4
print(sock.recvuntil("}\n\n").decode())
sock.sendlineafter("Answer: ", "verboten{b092eb225b07e17ba8a70b755ba97050:1541069606}")

# Q5
print(sock.recvuntil("}\n\n").decode())
sock.sendlineafter(
    "Answer: ",
    "verboten{ae679ca994f131ea139d42b507ecf457:4a47ee64b8d91be37a279aa370753ec9:870643eec523b3f33f6f4b4758b3d14c:c143b7a7b67d488c9f9945d98c934ac6:e6e6a0a39a4b298c2034fde4b3df302a}",
)

# Q6
print(sock.recvuntil("}\n\n").decode())
sock.sendlineafter("Answer: ", "verboten{2024-02-16-20-29-04:221436813}")

# Q7
print(sock.recvuntil("}\n\n").decode())
sock.sendlineafter("Answer: ", "verboten{2024-02-16-08-31-06}")

# Q8
print(sock.recvuntil("}\n\n").decode())
sock.sendlineafter("Answer: ", "verboten{Stuart:FutureKidsSchool:Howard}")

# Q9
print(sock.recvuntil("}\n\n").decode())
sock.sendlineafter("Answer: ", "verboten{830030:2024-02-16-23-24-43}")

sock.sh()
