# Float On:Misc:130pts
I cast my int into a double the other day, well nothing crashed, sometimes life's okay.  
We'll all float on, anyway: [float_on.c](float_on.c).  
Float on over to `/problems/2021/float_on` on the shell server, or connect with `nc shell.actf.co 21399`.  

# Solution
配布されたfloat_on.cは以下のようであった。  
```C
~~~
#define DO_STAGE(num, cond) do {\
    printf("Stage " #num ": ");\
    scanf("%lu", &converter.uint);\
    x = converter.dbl;\
    if(cond) {\
        puts("Stage " #num " passed!");\
    } else {\
        puts("Stage " #num " failed!");\
        return num;\
    }\
} while(0);

~~~

union cast {
    uint64_t uint;
    double dbl;
};

int main(void) {
    union cast converter;
    double x;

    DO_STAGE(1, x == -x);
    DO_STAGE(2, x != x);
    DO_STAGE(3, x + 1 == x && x * 2 == x);
    DO_STAGE(4, x + 1 == x && x * 2 != x);
    DO_STAGE(5, (1 + x) - 1 != 1 + (x - 1));

    print_flag();

    return 0;
}
```
uint64_tをdoubleにキャストしたものに演算を行い、結果を比較するプログラムのようだ。  
0、18446744073709551615、nan、infが怪しそうだ。  
doubleは符号1ビット、指数部11ビット、仮数部52ビットの64ビットとなっているため、uint64_tで任意のdoubleを再現できる。  
初めにStage1について考える。  
これは0を与えてやることで、0==-0となり容易に突破できる。  
次にStage2について考える。  
比較!=はnanで突破できそうだ。  
doubleでは指数部がすべて1であり仮数部がすべて0でない場合、nanとみなされる。  
符号は考慮しなくともよいので、18446744073709551615(1111111111111111111111111111111111111111111111111111111111111111)を与えてやれば-nan!=-nanとなり突破できる。  
次にStage3について考える。  
inf + 1 = inf、inf * 2 = infなので、xがinf(-inf)となるような入力を与えればよい。  
doubleでは指数部がすべて1であり仮数部がすべて0である場合、infとみなされる。  
よって18442240474082181120(1111111111110000000000000000000000000000000000000000000000000000)を与えると突破できる。  
次にStage4について考える。  
x + 1 == xでinf + 1 = infとするとx * 2 != xで困る。  
つまりx + 1がinfにならず、かつx * 2がinfになれば突破できる。  
2^53以降では偶数しか表現できないことより、14069245235905429505以降の入力でx + 1 == xが真となる。  
x * 2がinfになればよいので18442240474082181119を与えれば楽である。  
最後にStage5について考える。  
Stage2と同様に-nan!=-nanで突破できる。  
以下のように入力を行う。  
```bash
$ nc shell.actf.co 21399
Stage 1: 0
Stage 1 passed!
Stage 2: 18446744073709551615
Stage 2 passed!
Stage 3: 18442240474082181120
Stage 3 passed!
Stage 4: 18442240474082181119
Stage 4 passed!
Stage 5: 18446744073709551615
Stage 5 passed!
actf{well_we'll_float_on,_big_points_are_on_the_way}
```
flagが得られた。  

## actf{well_we'll_float_on,_big_points_are_on_the_way}