# clam clam clam:Misc:70pts
clam clam clam clam clam clam clam clam clam nc misc.2020.chall.actf.co 20204 clam clam clam clam clam clam  
Hint  
U+000D  

# Solution
nc misc.2020.chall.actf.co 20204をたたくと、以下のようにclamとmalcが流れ続ける。  
```bash
$ nc misc.2020.chall.actf.co 20204
clam{clam_clam_clam_clam_clam}
malc{malc_malc_malc_malc_malc}
clam{clam_clam_clam_clam_clam}
malc{malc_malc_malc_malc_malc}
clam{clam_clam_clam_clam_clam}
malc{malc_malc_malc_malc_malc}
clam{clam_clam_clam_clam_clam}
malc{malc_malc_malc_malc_malc}
~~~
```
ファイルにリダイレクトしてみる。  
```text:omg.txt
~~~
malc{malc_malc_malc_malc_malc}
clam{clam_clam_clam_clam_clam}
malc{malc_malc_malc_malc_malc}
clam{clam_clam_clam_clam_clam}
malc{malc_malc_malc_malc_malc}
type "clamclam" for salvation
clam{clam_clam_clam_clam_clam}
malc{malc_malc_malc_malc_malc}
~~~
```
type "clamclam" for salvationが所々に散らばっているのが分かる(改行コードがここだけ0Dだったので検索しても良い)。  
指示されたとおりclamclamとタイプするとflagが手に入る。  

## actf{cl4m_is_my_f4v0rite_ctfer_in_th3_w0rld}