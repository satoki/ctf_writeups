from ptrlib import *

logger.level = 0

while True:
    try:
        sock = Socket("nc 0.cloud.chals.io 26265")
        data = list(sock.recv(42))
        for i in range(len(data)):
             data[i] ^= 0x0A
        xor_data = bytes(data)
        print(xor_data)
        sock.close()
        if b"brck{" in xor_data:
            break
    except:
        pass