from string import ascii_uppercase,ascii_lowercase,digits,punctuation

# caesar_source.py
##################################################
def encode(plain):
  cipher=''
  for i in plain:
    index=letter.index(i)
    cipher=cipher+letter[(index+14)%len(letter)]
  return cipher

ascii_all=''
for i in range(len(ascii_uppercase)):
  ascii_all=ascii_all+ascii_uppercase[i]+ascii_lowercase[i]
letter=ascii_all+digits+punctuation
##################################################


cflag = open("caesar_output.txt").read()
flag = ""

for _ in range(len(cflag)):
    for i in letter:
        if cflag.startswith(encode(flag + i)):
            print(flag + i)
            flag += i