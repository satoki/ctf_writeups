# # <!--XXXXXXXXXX-->
The itsy-bitsy spider climbed up the water spout...  
nc 2020.redpwnc.tf 31284  
[itsy-bitsy.py](itsy-bitsy.py)  

# Solution
ncを行うと二つの数字を聞かれて、暗号化されたバイナリテキストが出てくる。  
```bash
$ nc 2020.redpwnc.tf 31284
Enter an integer i such that i > 0: 3
Enter an integer j such that j > i > 0: 9
Ciphertext: 0001000111111001011010011100110000000011000001001011110101111101110100100101100001000001101001000110110011111001000001110100101111100001001000001010101010101111110001101000111110011110000100000001110101100101111100011001111010100000011000101111000101101010001010011100111110110100010101110010100010010
```
ソースコードitsy-bitsy.pyは以下のようになっている。  
```python:pseudo-key.py
#!/usr/bin/env python3

from Crypto.Random.random import randint

def str_to_bits(s):
    bit_str = ''
    for c in s:
        i = ord(c)
        bit_str += bin(i)[2:]
    return bit_str

def recv_input():
    i = input('Enter an integer i such that i > 0: ')
    j = input('Enter an integer j such that j > i > 0: ')
    try:
        i = int(i)
        j = int(j)
        if i <= 0 or j <= i:
            raise Exception
    except:
        print('Error! You must adhere to the restrictions!')
        exit()
    return i,j

def generate_random_bits(lower_bound, upper_bound, number_of_bits):
    bit_str = ''
    while len(bit_str) < number_of_bits:
        r = randint(lower_bound, upper_bound)
        bit_str += bin(r)[2:]
    return bit_str[:number_of_bits]

def bit_str_xor(bit_str_1, bit_str_2):
    xor_res = ''
    for i in range(len(bit_str_1)):
        bit_1 = bit_str_1[i]
        bit_2 = bit_str_2[i]
        xor_res += str(int(bit_1) ^ int(bit_2))
    return xor_res

def main():
    with open('flag.txt','r') as f:
        flag = f.read()
    for c in flag:
        i = ord(c)
        assert i in range(2**6,2**7)
    flag_bits = str_to_bits(flag)
    i,j = recv_input()
    lb = 2**i
    ub = 2**j - 1
    n = len(flag_bits)
    random_bits = generate_random_bits(lb,ub,n)
    encrypted_bits = bit_str_xor(flag_bits,random_bits)
    print(f'Ciphertext: {encrypted_bits}')

if __name__ == '__main__':
    main()
```
ソースコードを読むと、flag.txtの中身をバイナリ化しそれをランダムなバイナリでXORしているようだ。  
ランダムなバイナリは入力数字の小さい方iと大きい方jで2^iから(2^j)-1までの乱数をバイナリ化したものであるらしい。  
一見すると総当たりしかないように思われる。  
しかし、適切にiとjの範囲を指定することで先頭ビットが1であることを使い元の文がわかる。  
```python
>>> bin(2**1)[2:]
'10'
>>> bin(2**2-1)[2:]
'11'

>>> bin(2**2)[2:]
'100'
>>> bin(2**3-1)[2:]
'111

>>> bin(2**3)[2:]
'1000'
>>> bin(2**4-1)[2:]
'1111'
```
2^1と(2^2)-1はともに一つ飛ばしで1となる。  
2^2と(2^3)-1の間の数字はともに二つ飛ばしで1となる。  
解析の例としては以下になる(XORなのでビット反転に注意)。  
```text
X = Not yet

c = 0011001100001000101000001101010011000011010010110000101001011001110100001001110110100010100101000001101100000000011001001001000111010100101100000111100001011000110100000001010101010000000001011011001111110010100101000100110000101101001111001101010110000001010000110000001011010000000101010011110100010
m = 11001101101100110000111001111111011X1X0X1X1X0X0X1X1X0X0X1X1X0X1X0X1X1X1X0X1X0X1X0X0X1X0X0X1X1X1X1X1X0X0X1X1X1X1X1X0X1X1X0X1X1X1X0X1X1X1X0X0X1X1X1X0X0X1X1X1X0X1X0X1X1X1X1X1X1X1X1X1X1X1X1X1X1X1X0X0X1X0X0X0X1X0X0X1X1X1X1X1X0X1X1X0X0X1X1X0X0X1X0X1X1X1X0X1X1X1X1X1X1X0X1X1X1X0X0X1X1X1X1X1X1X1X1X0X0X1111101

c = 0011001101011000111110001000000010010111010000100010001110111110000000101101100100010011100011100000111010100101101000001010000110110100111100010100110110111001000100010111000111110101000000101001001011100010100110010000110110001010011001101011010101100110110000110110111000100010010111010110100100100
m = 11001101101100110000111001111111011X1X001X1X010X1X110X0X111X0X110X1X111X0X100X1X010X1X000X1X101X1X110X0X111X1X101X0X111X0X111X1X011X1X110X0X111X1X010X1X111X0X100X1X111X1X101X1X101X1X101X1X111X0X001X0X000X1X010X1X111X1X110X1X110X0X111X0X001X0X101X1X001X1X111X1X110X1X111X0X011X1X111X1X101X1X010X1111101
```
これを以下のbit1X1X.pyで自動化する。  
```python:bit1X1X.py
import socket

host = "2020.redpwnc.tf"
port = 31284
text = "11001101101100110000111001111111011" + "X"*259 + "1111101"
# "flag{" + X + "}"
text = list(text)

try:
    for i in range(1, 300):
        print("[{}]".format(i))
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, port))
        client.recv(256)
        client.send(("{}\n".format(i)).encode('utf-8'))
        client.recv(256)
        client.send(("{}\n".format(i + 1)).encode('utf-8'))
        response = client.recv(1024)
        response = response.decode('utf-8')
        response = response.replace("Ciphertext: ", "")
        for j in range(len(text)):
            if j % (i + 1) == 0:
                text[j] = (str(int(response[j]) ^ 1))
        #print(response)
        #print("".join(text))
    text = "".join(text)
    print(text)
    for i in range(0, len(text), 7):
        print(chr(int(text[i: i+7], 2)), end="")
    print()
except:
    print("\n" + "".join(text))
```
実行するとflagが得られる。  
```bash
$ python bit1X1X.py
[1]
[2]
[3]
[4]
~~~
[296]
[297]
[298]
[299]
1100110110110011000011100111111101111000101101001111010011100111011111110110011001011100001110101111010011101110110011110111111101111111010111101001011111110010011011111110111110111010111111110100110100011001011011111111011111000011110100110010111100101011111111001111100001101111111010111101001111101
flag{bits_leaking_out_down_the_water_spout}
```

## flag{bits_leaking_out_down_the_water_spout}