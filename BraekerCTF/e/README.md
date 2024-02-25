# e:Programming / Misc:150pts
"Grrrrr". This robot just growls. The other bots tell you that it is angry because it can't count very high. Can you teach it how?  
![epsilon.jpg](epsilon.jpg)  

`nc 0.cloud.chals.io 30531`  

[e.cpp](e.cpp)  

Hint  
Read the decription again. What was your objective?  

# Solution
接続先とソースが渡される。  
ソースは以下の通りであった。  
```cpp
#include <iostream>
#include <random>  
#include <sys/auxv.h>
using namespace std;


void add_user_input(vector<float> *n_arr, string msg) {
	float input;
	cout << msg << endl;
	cin >> input;
	n_arr->push_back(input);
}

float get_user_input(string msg) {
	float input;
	cout << msg << endl;
	cin >> input;
	return input;
}

int fail() {
	cout << "That was a fail" << endl;
	return 0;
}


bool flow_start() {

	// Get user input
	float a = get_user_input("Number that is equal to two: ");

	// Can't be two
	if (a <= 2)
		return false;

	// Check if equal to 2
	return (unsigned short)a == 2;
}


bool round_2() {

	float total = 0;

	// Sum these numbers to 0.9
	for (int i = 0; i < 9; i++)
		total += 0.1;

	// Add user input
	total += get_user_input("Number to add to 0.9 to make 1: ");

	// Check if equal to one
	return total == 1.0;
}


bool level_3() {

	float total = 0;

	unsigned int *seed;
	vector<float> n_arr;

	// Random seed
	seed = (unsigned int *)getauxval(AT_RANDOM);
	srand(*seed);

	// Add user input
	add_user_input(&n_arr, "Number to add to array to equal zero: ");

	// Add many random integers
	for (int i = 0; i < 1024 * (8 + rand() % 1024); i++)
		n_arr.push_back((rand() % 1024) + 1);

	// Add user input
	add_user_input(&n_arr, "Number to add to array to equal zero: ");

	// Get sum
	for (int i = 0; i < n_arr.size(); i++)
		total += n_arr[i];

	// Check if equal to zero
	return total == 0;
}




int main(void) {

	cout << "Welcome!" << std::endl;

	if (! flow_start() )
		return fail();

	cout << "Well done! This is the second round:" << std::endl;

	if (! round_2() )
		return fail();

	cout << "Great! Up to level three:" << std::endl;

	if (! level_3() )
		return fail();

	cout << "Well done! Here is the flag: brck{not_the_flag}" << std::endl;


	return 0;
}
```
3つのステージをクリアするとフラグが得られるようだ。  
1つ目は以下のようだ。  
```cpp
bool flow_start() {

	// Get user input
	float a = get_user_input("Number that is equal to two: ");

	// Can't be two
	if (a <= 2)
		return false;

	// Check if equal to 2
	return (unsigned short)a == 2;
}
```
`float`では2より大きく、`unsigned short`では2になる数値を入力すればよい。  
`unsigned short`の最大値は65535であるので、オーバーフローする`float`値を与えれば条件を満たせる。  
`65538`を入力すればよい。  
2つ目は以下のようだ。  
```cpp
bool round_2() {

	float total = 0;

	// Sum these numbers to 0.9
	for (int i = 0; i < 9; i++)
		total += 0.1;

	// Add user input
	total += get_user_input("Number to add to 0.9 to make 1: ");

	// Check if equal to one
	return total == 1.0;
}
```
9回のループで、`float`の変数に0.1ずつ加算して0.9にしている。  
最後にユーザ入力を加算して、1.0にすればよい。  
ただし、`0.1`の入力では誤差により1.0にならない。  
誤差を計算するプログラムを書く。  
```cpp
#include <iomanip>
#include <iostream>

int main() {
    float total = 0;

    for (int i = 0; i < 9; i++)
        total += 0.1;

    float requiredToAdd = 1.0 - total;

    std::cout << std::fixed << std::setprecision(30) << requiredToAdd << std::endl;

    return 0;
}
```
実行する。  
```bash
$ g++ round_2.cpp -o round_2
$ ./round_2
0.099999904632568359375000000000
```
`0.099999904632568359375`を入力すればよいようだ。  
3つ目は以下のようだ。  
```cpp
bool level_3() {

	float total = 0;

	unsigned int *seed;
	vector<float> n_arr;

	// Random seed
	seed = (unsigned int *)getauxval(AT_RANDOM);
	srand(*seed);

	// Add user input
	add_user_input(&n_arr, "Number to add to array to equal zero: ");

	// Add many random integers
	for (int i = 0; i < 1024 * (8 + rand() % 1024); i++)
		n_arr.push_back((rand() % 1024) + 1);

	// Add user input
	add_user_input(&n_arr, "Number to add to array to equal zero: ");

	// Get sum
	for (int i = 0; i < n_arr.size(); i++)
		total += n_arr[i];

	// Check if equal to zero
	return total == 0;
}
```
`float`の配列に一度目のユーザ入力を追加し、その後に乱数を大量に追加し、最後に二度目のユーザ入力を追加している。  
最終的に配列の総和が0になればよいようだ。  
乱数が不明なため単純な計算で総和を0にすることはできない。  
ここで、巨大な整数を扱うことで、乱数を誤差と判断させるアイデアを思いつく。  
適当だが、一度目に`10000000000000000000`を入力し、二度目に`-10000000000000000000`を入力してやればよい。  
一連の流れを以下のように行う。  
```bash
$ nc 0.cloud.chals.io 30531
Welcome!
Number that is equal to two:
65538
Well done! This is the second round:
Number to add to 0.9 to make 1:
0.099999904632568359375
Great! Up to level three:
Number to add to array to equal zero:
10000000000000000000
Number to add to array to equal zero:
-10000000000000000000
Well done! Here is the flag: brck{Th3_3pS1l0n_w0rkS_In_M15t3riOuS_W4yS}
```
flagが得られた。  

## brck{Th3_3pS1l0n_w0rkS_In_M15t3riOuS_W4yS}