from string import ascii_uppercase,ascii_lowercase,digits,punctuation

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
plain_text='UECTF{SECRET}'
cipher_text=encode(plain_text)
print(cipher_text)
