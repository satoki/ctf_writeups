# Steam Locomotive:Miscellaneous:50pts
I keep accidentally mistyping the `ls` command!  

**Connect with:**  
```
# Password is "userpass"
ssh -p 30061 user@challenge.nahamcon.com
```

# Solution
sshの接続先のみが与えられているので、接続する。  
```
$ ssh -p 30061 user@challenge.nahamcon.com
user@challenge.nahamcon.com's password:

                          (  ) (@@) ( )  (@)  ()    @@    O     @     O     @      O
                     (@@@)
                 (    )
              (@@@@)

            (   )
        ====        ________                ___________
    _D _|  |_______/        \__I_I_____===__|_________|
     |(_)---  |   H\________/ |   |        =|___ ___|      _________________
     /     |  |   H  |  |     |   |         ||_| |_||     _|                \_____A
    |      |  |   H  |__--------------------| [___] |   =|                        |
    | ________|___H__/__|_____/[][]~\_______|       |   -|                        |
    |/ |   |-----------I_____I [][] []  D   |=======|____|________________________|_
  __/ =| o |=-~~\  /~~\  /~~\  /~~\ ____Y___________|__|__________________________|_
   |/-=|___|=O=====O=====O=====O   |_____/~\___/          |_D__D__D_|  |_D__D__D_|
    \_/      \__/  \__/  \__/  \__/      \_/               \_/   \_/    \_/   \_/

```
slコマンドが走って終了する。  
入力もなにも受け付けないため操作ができない。  
ここでsshのオプションとしてシェルを指定することができたことを思い出す。  
以下の通りに行う。  
```bash
$ ssh -p 30061 user@challenge.nahamcon.com -t /bin/sh
user@challenge.nahamcon.com's password:
~ $ ls
flag.txt
~ $ cat flag.txt
flag{4f9b10a81141c7a07a494c28bd91d05b}
```
shellが起動するのでファイルを読み取るとflagが得られた。  

## flag{4f9b10a81141c7a07a494c28bd91d05b}