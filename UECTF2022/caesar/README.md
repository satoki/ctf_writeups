# caesar:MISC:100pts
ガイウス・ユリウス・カエサル Gaius Iulius Caesar  

[caesar_source.py](caesar_source.py)　[caesar_output.txt](caesar_output.txt)  

# Solution
pyとtxtが配布される。  
問題名からシーザー暗号だと推測でき。案の定txtは`2LJ0MF0o&*E&zEhEi&1EKpmm&J3s1Ej)(zlYG`という意味不明な文字であった。  
pyを見ると以下のようであった。  
```python
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
```
いろいろと書かれているが、`plain_text`を暗号化しているようだ。  
総当たりで一文字ずつ特定できると考え、以下のsolverを書く。  
```python
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
```
実行する。  
```bash
$ python solver.py
U
UE
UEC
~~~
UECTF{Th15_1s_a_b1t_Diff1Cult_c43se
UECTF{Th15_1s_a_b1t_Diff1Cult_c43seR
UECTF{Th15_1s_a_b1t_Diff1Cult_c43seR}
```
flagが得られた。  

## UECTF{Th15_1s_a_b1t_Diff1Cult_c43seR}