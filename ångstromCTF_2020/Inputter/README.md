# Inputter:Misc:100pts
Clam really likes challenging himself. When he learned about all these weird unprintable ASCII characters he just HAD to put it in [a challenge](inputter). Can you satisfy his knack for strange and hard-to-input characters? [Source](inputter.c).  
Find it on the shell server at /problems/2020/inputter/.  
Hint  
There are ways to run programs without using the shell.  

# Solution
ソースを見るとコマンドライン引数に入力が難しいものが指定されている。  
flagは運営サーバーのflag.txtに記述されているようだ。  
pythonで引数を渡してやれば解決する。  
```bash
@actf:~$ cd /problems/2020/inputter/
@actf:/problems/2020/inputter$ ls
flag.txt  inputter  inputter.c
@actf:/problems/2020/inputter$ python3
~~~
>>> import subprocess
>>> input_text = "\x00\x01\x02\x03".encode("utf-8")
>>> subprocess.run(["./inputter", " \n'\"\x07"], input=input_text)
You seem to know what you're doing.
actf{impr4ctic4l_pr0blems_c4ll_f0r_impr4ctic4l_s0lutions}
CompletedProcess(args=['./inputter', ' \n\'"\x07'], returncode=0)
```

## actf{impr4ctic4l_pr0blems_c4ll_f0r_impr4ctic4l_s0lutions}