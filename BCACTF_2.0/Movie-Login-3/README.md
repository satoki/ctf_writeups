# Movie-Login-3:webex:200pts
I think the final addition to the Gerard series is coming out! I heard the last few movies got their poster leaked. I'm pretty sure they've increased their security, though. Could you help me find the poster again?  
[denylist.json](denylist.json)  
[http://web.bcactf.com:49162/](http://web.bcactf.com:49162/)  
  
Hint 1 of 2  
Does there seem to be anything different about this problem?  
Hint 2 of 2  
How can you get around the new keywords being detected?  

# Solution
[Movie-Login-2](../Movie-Login-2)と同様の問題のようだ。  
denylist.jsonが以下のように更新されていた。  
```json:denylist.json
[
    "and",
    "1",
    "0",
    "true",
    "false",
    "/",
    "*",
    "=",
    "xor",
    "null",
    "is",
    "<",
    ">"
]
```
`true`が使えなくなっているが、`' OR 2 --`とすればよいだけである。  
[flag.png](site/flag.png)  
ログインに成功すると、flagが表示された。  

## bcactf{gu3ss_th3r3s_n0_st0pp1ng_y0u!}