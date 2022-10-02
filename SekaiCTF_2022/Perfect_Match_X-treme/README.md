# Perfect Match X-treme:Reverse:100pts
Can you qualify Fall Guy’s *Perfect Match* and get the flag?  
<iframe src="https://www.youtube.com/embed/edifg0uMzxU"></iframe>  

[Perfect_Match_X-treme.zip](Perfect_Match_X-treme.zip)  

# Solution
何らかのゲームが配布される。  
初手は解凍し、grepを行う。  
```bash
$ unzip Perfect_Match_X-treme.zip
~~~
$ grep -r SEKAI
Binary file Build/PerfectMatch_Data/level0 matches
```
`Build/PerfectMatch_Data/level0`がヒットしたため、stringsを行う。  
```bash
$ strings Build/PerfectMatch_Data/level0
~~~
L>333?
SEKAI{F4LL_GUY5_
fff?fff?
Qualified!
1LL3G4L}
H3CK_15_
Horizontal
Vertical
Submit
Cancel
Analog X
Analog Y
=333?
Jump
Sprint
```
明らかにフラグの一部がみられる。  
うまく文章が通るように再構成すると`SEKAI{F4LL_GUY5_H3CK_15_1LL3G4L}`となりこれがflagであった。  

## SEKAI{F4LL_GUY5_H3CK_15_1LL3G4L}