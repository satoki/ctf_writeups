# アンケート:Welcome:0pts
もうええわ！って思ったらアンケートにご協力お願いします！ → [https://forms.gle/rAsPHRznXcvtkzPr8](https://forms.gle/rAsPHRznXcvtkzPr8)  
（アンケート送信後にフラグが表示されます）  

# Solution
アンケートは後で答えるとして、フラグの奪取をめざす。  
```bash
$ curl 'https://forms.gle/rAsPHRznXcvtkzPr8' -sL | grep -o 'flag{.*}'
flag{h499y_n3w_y34r_2024}
```
curlで取得できた(Writeupまかせろり)。  

## flag{h499y_n3w_y34r_2024}