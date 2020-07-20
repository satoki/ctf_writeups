shift_table = "abcdefghijklmnopqrstuvwxyz0123456789{}_"
def decrypt(text: str, shift: int) -> str:
    assert  0 <= shift <= 9
    res = ""
    for c in text:
        res += shift_table[(shift_table.index(c)-shift)%len(shift_table)]
    return res

flag = "6}bceijnob9h9303h6yg896h0g896h0g896h01b40g896hz"
while flag[0].isdigit():
	flag = decrypt(flag[1:], int(flag[0]))
	print(flag)