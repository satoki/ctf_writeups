
inp = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_{}"
outp = "dBFS4f}jZE5gRsAKOplm20xt8hwcevoyGz1TJ{VDMQ39iquC7WXN_HLYUaPkr6Ibn"
text = "j4teqybvAskIE2S}4IdIc_M5IB8IHmlIF_0Ypn"

flag = []
for i in range(len(text)):
	for j in range(len(outp)):
		if text[i] == outp[j]:
			flag.append(inp[j])

print("".join(flag))