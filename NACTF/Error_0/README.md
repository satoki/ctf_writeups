# Error 0:Cryptography:150pts
Rahul has been trying to send a message to me through a really noisy communication channel. Repeating the message 101 times should do the trick!  
[enc.txt](enc.txt)  

# Solution
enc.txtが渡される。  
中身を[Binary to Text Translator](https://www.rapidtables.com/convert/number/binary-to-ascii.html)にかけてみるが、文字化けしている。  
どうやらノイズのある環境で101回メッセージを送っているようだ。  
txtの中身を101回分に分割して各ビットの統計を取ればよい。  
以下のero.pyで行う。  
```python:ero.py
flag = open("enc.txt").read()
msg = 101

msglen = int(len(flag)/msg)
msgs = [[]] * msg

for i in range(msg):
    msgs[i] = flag[:msglen]
    flag = flag[msglen:]

for i in range(msglen):
    zero = 0
    for j in range(msg):
        if msgs[j][i] == "0":
            zero += 1
    if (msg/2) < zero:
        print(0, end="")
    else:
        print(1, end="")
print()
```
実行する。  
```bash
$ python ero.py
0110111001100001011000110111010001100110011110110110111000110000001100010111001101111001010111110110111000110000001100010011001101101010010111110111110001011100011111000010100000101001011111000010010000100111001011110111110100001010
```
再度[Binary to Text Translator](https://www.rapidtables.com/convert/number/binary-to-ascii.html)にかけると`nactf{n01sy_n013j_|\|()|$'/}`となった。  
これがflagである。  

## nactf{n01sy_n013j_|\|()|$'/}