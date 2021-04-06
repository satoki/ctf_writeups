# Archaic:Misc:50pts
The archaeological team at ångstromCTF has uncovered an archive from over 100 years ago! Can you read the contents?  
Access the file at `/problems/2021/archaic/archive.tar.gz` on the shell server.  
Hint  
What is a .tar.gz file?  

# Solution
問題サーバにarchive.tar.gzが置かれているようだ。  
アクセスして解凍する。  
```bash
$ ssh team7901@shell.actf.co
team7901@shell.actf.co's password:
Welcome to the
                       _                            _    __
   ()                 | |                          | |  / _|
  __ _ _ __   __ _ ___| |_ _ __ ___  _ __ ___   ___| |_| |_
 / _` | '_ \ / _` / __| __| '__/ _ \| '_ ` _ \ / __| __|  _|
| (_| | | | | (_| \__ \ |_| | | (_) | | | | | | (__| |_| |
 \__,_|_| |_|\__, |___/\__|_|  \___/|_| |_| |_|\___|\__|_|
              __/ |
             |___/

shell server!

*==============================================================================*
*  Please be respectful of other users. Abuse may result in disqualification.  *
*Data can be wiped at ANY TIME with NO WARNING. Keep backups of important data!*
*==============================================================================*
Last login: Tue Apr  6 09:15:06 2021 from 219.126.191.19
team7901@actf:~$ tar -zxvf /problems/2021/archaic/archive.tar.gz
flag.txt
tar: flag.txt: implausibly old time stamp 1921-04-01 22:45:12
team7901@actf:~$ cat flag.txt
cat: flag.txt: Permission denied
team7901@actf:~$ chmod 777 flag.txt
team7901@actf:~$ cat flag.txt
actf{thou_hast_uncovered_ye_ol_fleg}
```
flag.txtの中にflagが書かれていた。  

## actf{thou_hast_uncovered_ye_ol_fleg}