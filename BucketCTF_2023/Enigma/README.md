# Enigma:CRYPTO:484pts
I found an old enigma machine and was messing around with it. I put a secret into it but forgot it. I remember some of the settings and have the output. Model: `M3` Reflector: `B` Rotors: `I II III` Plugboard: `AT BS DE FM IR KN LZ OW PV XY` Output: `rvvrw dxyfi cctev o`  
There has been a new flag that some teams already found.  
The solution is not in the normal `bucket{}` syntax. Remove spaces.  
Lowercase  

# Solution
エニグマの各設定と暗号文が与えられている。  
ただし、リングと呼ばれる部分の設定(アルファベット3文字分)が分からないようだ。  
通常のフラグ形式と異なるようだが、おそらく`backet`が含まれていると予想し、以下のsolver.pyで総当たりする。  
```python
from enigma.machine import EnigmaMachine

for a in range(1, 26):
    for b in range(1, 26):
        for c in range(1, 26):
            machine = EnigmaMachine.from_key_sheet(
                rotors="I II III",
                reflector="B",
                ring_settings=[a, b, c],
                plugboard_settings="AT BS DE FM IR KN LZ OW PV XY"
            )
            plaintext = machine.process_text("rvvrwdxyficctevo").lower()
            if "bucket" in plaintext:
                print(plaintext)
```
実行する。  
```bash
$ python solver.py
bucketngmcdbdbaa
```
それらしくない文字列が出てきたが、試しに入力するとflagであった。  

## bucketngmcdbdbaa