# Welcome to the Casino:misc:150pts
Can you get three-of-a-kind on this slot machine? Let's find out!  
`nc misc.bcactf.com 49156` [Copy](https://play.bcactf.com/challenges/73da2ad6-8fd1-4026-9e6a-058f9dd581dd/solve#)  
Hint 1 of 4  
There's got to be a faster way than to connect manually, right?  
Hint 2 of 4  
Can you use a tool to make your computer connect for you?  
Hint 3 of 4  
The flag is in the format `bcactf{...}`. Use that to your advantage when parsing output.  
Hint 4 of 4  
Once you're connecting as fast as you can, how can you get even more connections?  

# Solution
ncでアクセスしてみるとキーを押せと言われ謎のスピンが始まる。  
```bash
$ nc misc.bcactf.com 49156
 /$$                           /$$
| $$                          | $$
| $$       /$$   /$$  /$$$$$$$| $$   /$$ /$$   /$$
| $$      | $$  | $$ /$$_____/| $$  /$$/| $$  | $$
| $$      | $$  | $$| $$      | $$$$$$/ | $$  | $$
| $$      | $$  | $$| $$      | $$_  $$ | $$  | $$
| $$$$$$$$|  $$$$$$/|  $$$$$$$| $$ \  $$|  $$$$$$$
|________/ \______/  \_______/|__/  \__/ \____  $$
                                         /$$  | $$
                                        |  $$$$$$/
                                         \______/
 /$$                   /$$     /$$
| $$                  | $$    | $$
| $$        /$$$$$$  /$$$$$$ /$$$$$$    /$$$$$$
| $$       /$$__  $$|_  $$_/|_  $$_/   /$$__  $$
| $$      | $$  \ $$  | $$    | $$    | $$  \ $$
| $$      | $$  | $$  | $$ /$$| $$ /$$| $$  | $$
| $$$$$$$$|  $$$$$$/  |  $$$$/|  $$$$/|  $$$$$$/
|________/ \______/    \___/   \___/   \______/



Welcome to the Lucky Lotto Slot Machine!
Let's see if you're today's big winner!
Enter the letter "d" to pull the lever...
d
Spinning...
           [[[ e ]]]
           [[[ p ]]]
           [[[ i ]]]

You didn't win anything. Try matching more letters next time!

Come back next time!
```
揃えばよいと思われるが、実行から結果が出るまで少しの時間が必要なようだ。  
また、キーは実行ごとに任意の小文字アルファベットが指定されるようだ。  
以下のsssssssssspin.shを用いて一度に複数回実行すればよい。  
```sh:sssssssssspin.sh
echo -e "abcdefghijklmnopqrstuvwxyz\n" | nc misc.bcactf.com 49156 | grep ctf &
echo -e "abcdefghijklmnopqrstuvwxyz\n" | nc misc.bcactf.com 49156 | grep ctf &
~~~
echo -e "abcdefghijklmnopqrstuvwxyz\n" | nc misc.bcactf.com 49156 | grep ctf &
echo -e "abcdefghijklmnopqrstuvwxyz\n" | nc misc.bcactf.com 49156 | grep ctf &
```
実行する。  
```bash
$ ./sssssssssspin.sh
$ bcactf{y0u_g0t_1ucKy_af23dd97g64n}
```
flagが出力された。  

## bcactf{y0u_g0t_1ucKy_af23dd97g64n}