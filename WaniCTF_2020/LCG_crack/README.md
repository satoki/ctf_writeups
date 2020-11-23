# LCG crack:Crypto:pts
安全な暗号は安全な乱数から  
nc lcg.wanictf.org 50001  
[server.py](server.py)  

# Solution
server.pyがサーバ側で動いているようだ。  
Crypto問だが暗号は解けそうにないので筋力を使う。  
以下の部分に注目する。  
```python
~~~
        # Guess
        elif choice == 2:
            for cnt in range(1, 11):
                print(f"[{cnt}/10] Guess the next number!")
                try:
                    guess = int(input("> "))
                except ValueError:
                    print("Please enter an integer\n\n\n")
                    continue
                if guess == rng.next():
                    print(f"Correct! ")
                    cnt += 1
                else:
                    print(f"Wrong... Try again!")
                    break
            else:
                print(f"Congratz!  {flag}")
                break
~~~
```
elseに入るとbreakされるようだが、exceptでも正解と同じ振る舞いをしている(rangeなので)。  
毎回intでない入力を与えてエラーを発生させ続ければよい。  
以下のようにエンターを入力しまくり、ハックする。  
```bash
$ nc lcg.wanictf.org 50001


     :::       .,-:::::  .,-:::::/
     ;;;     ,;;;'````',;;-'````'
     [[[     [[[       [[[   [[[[[[/
     $$'     $$$       "$$c.    "$$
    o88oo,.__`88bo,__,o,`Y8bo,,,o88o
    """"YUMMM  "YUMMMMMP" `'YMUP"YMM



      +=============================+
      | 1. Generate the next number |
      | 2. Guess the next number    |
      | 3. Exit                     |
      +=============================+

 - Guess the numbers in a row, and I'll give you a flag!
> 2
 - [1/10] Guess the next number!
>
Please enter an integer



 - [2/10] Guess the next number!
>
Please enter an integer



 - [3/10] Guess the next number!
>
Please enter an integer



 - [4/10] Guess the next number!
>
Please enter an integer



 - [5/10] Guess the next number!
>
Please enter an integer



 - [6/10] Guess the next number!
>
Please enter an integer



 - [7/10] Guess the next number!
>
Please enter an integer



 - [8/10] Guess the next number!
>
Please enter an integer



 - [9/10] Guess the next number!
>
Please enter an integer



 - [10/10] Guess the next number!
>
Please enter an integer



Congratz!  FLAG{y0u_sh0uld_buy_l0tt3ry_t1ck3ts}


```
flagが得られた。  

## FLAG{y0u_sh0uld_buy_l0tt3ry_t1ck3ts}