c = 0xae27eb3a148c3cf031079921ea3315cd27eb7d02882bf724169921eb3a469920e07d0b883bf63c018869a5090e8868e331078a68ec2e468c2bf13b1d9a20ea0208882de12e398c2df60211852deb021f823dda35079b2dda25099f35ab7d218227e17d0a982bee7d098368f13503cd27f135039f68e62f1f9d3cea7c
c = bin(c)[2:]
c = [c[i: i+40] for i in range(0, len(c), 40)]

a = "0110000101100011011101000110011001111011" #actf{

keys = []
for i in c:
    keys.append(int(a, 2) ^ int(i, 2))

flags = []
for i in keys:
    tmp = []
    for j in c:
        flag = i ^ int(j, 2)
        flag = flag.to_bytes((flag.bit_length() + 7) // 8, byteorder='big')
        try:
            flag = flag.decode()
        except:
            break
        tmp.append(flag)
    flags.append("".join(tmp))

for i in flags:
    if "actf{" in i:
        print(i)