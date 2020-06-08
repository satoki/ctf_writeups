# Teleport:Misc:300pts
Challenge instance ready at 95.216.233.106:34351.  
One of our admins plays a strange game which can be accessed over TCP. He's been playing for a while but can't get the flag! See if you can help him out.  
[teleport.py](teleport.py)  

# Solution
ncすると座標を移動できるゲームなようだ。  
ただしユークリッド距離で10未満しか移動できない。  
```bash
$
satoki@SatoPC:~$ nc 95.216.233.106 34351
Your player is at 0,0
The flag is at 10000000000000, 10000000000000
Enter your next position in the form x,y
You can move a maximum of 10 metres at a time
Current position: 0.0, 0.0
Enter next position(maximum distance of 10): 1,1
Current position: 1.0, 1.0
Enter next position(maximum distance of 10): 5,5
Current position: 5.0, 5.0
Enter next position(maximum distance of 10): 1000,1000
You moved too far
Current position: 5.0, 5.0
~~~
```
ソースは以下のようになっている。  
```python:teleport.py
import math

x = 0.0
z = 0.0
flag_x = 10000000000000.0
flag_z = 10000000000000.0
print("Your player is at 0,0")
print("The flag is at 10000000000000, 10000000000000")
print("Enter your next position in the form x,y")
print("You can move a maximum of 10 metres at a time")
for _ in range(100):
    print(f"Current position: {x}, {z}")
    try:
        move = input("Enter next position(maximum distance of 10): ").split(",")
        new_x = float(move[0])
        new_z = float(move[1])
    except Exception:
        continue
    diff_x = new_x - x
    diff_z = new_z - z
    dist = math.sqrt(diff_x ** 2 + diff_z ** 2)
    if dist > 10:
        print("You moved too far")
    else:
        x = new_x
        z = new_z
    if x == 10000000000000 and z == 10000000000000:
        print("ractf{#####################}")
        break
```
100回のループでは10000000000000,10000000000000には到達できそうにない。  
入力から現在地を引いている部分に注目する。  
```python
~~~
    diff_x = new_x - x
    diff_z = new_z - z
    dist = math.sqrt(diff_x ** 2 + diff_z ** 2)
    if dist > 10:
        print("You moved too far")
    else:
~~~
```
この手のものとして、inf、1e100、nanなどでの動作が思わぬ落とし穴を生むが、今回はnanのようだ。  
```bash
$ python
~~~
>>> import math
>>> math.nan
nan
>>> math.nan - 0
nan
>>> math.sqrt(math.nan ** 2 + math.nan ** 2)
nan
>>> math.nan > 10
False
>>> 10000000000000 - math.nan
nan
```
つまりnanを入力することにより、new_x、new_zがnan、nanになるためif dist > 10を通り抜けx、zはnanになる。  
さらに10000000000000を入力することで、new_x、new_zは10000000000000、10000000000000になるがif文をバイパスできる。  
```bash
$ nc 95.216.233.106 34351
Your player is at 0,0
The flag is at 10000000000000, 10000000000000
Enter your next position in the form x,y
You can move a maximum of 10 metres at a time
Current position: 0.0, 0.0
Enter next position(maximum distance of 10): nan,nan
Current position: nan, nan
Enter next position(maximum distance of 10): 10000000000000,10000000000000
ractf{fl0at1ng_p01nt_15_h4rd}
```
flagはテレポート先にあった。  

## ractf{fl0at1ng_p01nt_15_h4rd}