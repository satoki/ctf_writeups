# tshark -r clocks_medium.pcap -T fields -e frame.time 'icmp.type==8' > times.txt
from Crypto.Util.number import long_to_bytes

times = open("times.txt").read().split("\n")

flag_bin = ""
prev_t = 0

for i in times[:-1]:
    time = float(i.split(" ")[4].split(":")[2])
    delta = time - prev_t
    if delta < 0:
        delta += 60
    if delta > 0.5:
        flag_bin += "1"
    else:
        flag_bin += "0"
    prev_t = time

flag_bin = flag_bin[1:]

print(long_to_bytes(int(flag_bin, 2)).decode())