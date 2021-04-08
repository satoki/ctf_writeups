# Keysar v2:Crypto:40pts
Wow! Aplet sent me a message... he said he encrypted it with a key, but lost it. Gotta go though, I have biology homework!  
[Source](chall.py) [Output](out.txt)  

# Solution
シーザー暗号のようだ。  
配布されたchall.pyを見ると鍵の一部分はアルファベットの連続になっていることがわかる。  
この長さの文が与えられていれば、気合で読める。  
鍵を部分的に復元してみる。(c:暗号文、t:平文、g:推測文)  
**Step1**  
c qufx{  
t actf{  
alp abcdefghijklmnopqrstuvwxyz  
key q.u..x.............f......  
**Step2**  
c quutcvbmy ft  
t acc?????? t?  
g according to  
alp abcdefghijklmnopqrstuvwxyz  
key q.uv.xy.b....mt..c.f......  
**Step3**  
アルファベットが連続になっているので  
alp abcdefghijklmnopqrstuvwxyz  
key q.uvwxyzb....mt..c.f......  
**Step4**  
c qii  
t a??  
g all  
alp abcdefghijklmnopqrstuvwxyz  
key q.uvwxyzb..i.mt..c.f......  
**Step5**  
c qgftrqfbuqiio  
t a?to?aticall?  
g automatically  
alp abcdefghijklmnopqrstuvwxyz  
key q.uvwxyzb..irmt..c.fg...o.  
**Step6**  
アルファベットが連続になっているので  
alp abcdefghijklmnopqrstuvwxyz  
key qsuvwxyzb..irmt..c.fg...o.  
**Step7**  
c brhtddbsiw  
t im?o??ibly  
g impossibly  
alp abcdefghijklmnopqrstuvwxyz  
key qsuvwxyzb..irmth.cdfg...o.  
**StepF**  
c qufx{awowvuqwdqcrtcwibawdgsdfbfgfbtm}  
t actf{?eyedcaesarmoreli?esubstitution}  
g actf{keyedcaesarmorelikesubstitution}  
alp abcdefghijklmnopqrstuvwxyz  
key qsuvwxyzb..irmth.cdfg...o.  
flagが推測できた。

## actf{keyedcaesarmorelikesubstitution}  