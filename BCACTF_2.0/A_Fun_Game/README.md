# A Fun Game:rev:100pts
A really fun game where you have to type the correct letter 1000 times to get the flag! It won't take that long, right? It's not like there's another way to do it...  
Note, The executable is built for Linux and can be run with `mono Game.exe`  
[Game.exe](Game.exe)  
  
Hint 1 of 2  
Is it possible to modify the variable storing your points?  
Hint 2 of 2  
What does a program like GameConqueror or CheatEngine do?  

# Solution
exeが配られるが、monoで実行するもののようだ。  
実行すると以下のようであった。  
```cmd
>mono Game.exe
Hello!
Write the correct letter 1,000 times to get the flag!
Not that hard, right?
Type '0' to stop.
Type the letter 't':
a
Incorrect. Current Points: 0
Type the letter 'k':
k
Correct! Current points: 1
Type the letter 'r':
```
表示されたものを入力するだけのようだ。  
以下のmyhands.pyでキー操作をし、自動で入力を行う。  
```python:myhands.py
import time
import pyautogui
import pyperclip

time.sleep(5)

while True:
    pyautogui.hotkey("shift", "up")
    pyautogui.hotkey("ctrlleft", "c")
    text = pyperclip.paste().replace("Type the letter '", "").replace("':", "").replace("\n", "")
    pyperclip.copy(text)
    pyautogui.hotkey("ctrlleft", "v")
    print(text)
```
別ウィンドウで実行し、5秒以内に対象ウィンドウを選択する。  
実行結果は以下のようになった。  
```cmd
>mono Game.exe
Hello!
Write the correct letter 1,000 times to get the flag!
Not that hard, right?
Type '0' to stop.
Type the letter 'g':
g
Correct! Current points: 1
Type the letter 'd':
d
Correct! Current points: 2
Type the letter 'h':
h
~~~
Correct! Current points: 998
Type the letter 'i':
i
Correct! Current points: 999
Type the letter 'd':
d
Correct! Current points: 1000
Here's your flag: bcactf{h0p3fu1ly_y0U_d1dNt_actUa1ly_tYpe_1000_1ett3rs}
```
flagが得られた。  

## bcactf{h0p3fu1ly_y0U_d1dNt_actUa1ly_tYpe_1000_1ett3rs}