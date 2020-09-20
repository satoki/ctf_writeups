rotflag = "ndldie_al_aqk_jjrnsxee"

print("DUCTF{",end="")

i = 15
for j in rotflag:
        m = (ord(j) - ord('a') + i) % 26
        ans = chr(m + ord('a'))
        if j == "_":
            ans = j
        print(ans,end="")
        i -= 1

print("}")