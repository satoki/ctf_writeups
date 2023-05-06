# web_assembly:Reversing:213pts
ブラウザ上でC++を動かすことに成功しました！！ 正しいユーザ名とパスワードを入力するとフラグがゲットできます。  
I successfully ran C++ in the browser!! Enter the correct username and password to get the flag.  
[https://wasm-rev.wanictf.org](https://wasm-rev.wanictf.org/)  

---

注意: 作問におけるミスにより、フラグは`Flag{`から始まり`}`で終わります。ご迷惑をおかけして申し訳ありません。  
Note: This flag starts `Flag{` and ends `}`. Sorry for the inconvenience.  

# Solution
URLが渡されるのでアクセスすると、emscriptenで作られたwasmが動いているようだ。  
`name`と`password`をpromptで聞かれるがわからない。  
ひとまず、開発者ツールのデバッガーからwasmの中身を見てやる。  
すると末尾に以下のようなデータが見られた。  
```wasm
  (data (i32.const 65536) "3r!}\00infinity\00February\00January\00July\00Thursday\00Tuesday\00Wednesday\00Saturday\00Sunday\00Monday\00Friday\00May\00%m/%d/%y\004n_3x\00-+   0X0x\00-0X+0X 0X-0x+0x 0x\00Nov\00Thu\00unsupported locale for standard input\00August\00Oct\00Sat\000us\00Apr\00vector\00October\00November\00September\00December\00ios_base::clear\00Mar\00p_0n_Br\00Sep\003cut3_Cp\00%I:%M:%S %p\00Sun\00Jun\00Mon\00nan\00Jan\00Jul\00ll\00April\00Fri\00March\00Aug\00basic_string\00inf\00%.0Lf\00%Lf\00true\00Tue\00false\00June\00Wed\00Dec\00Feb\00Fla\00ckwajea\00%a %b %d %H:%M:%S %Y\00POSIX\00%H:%M:%S\00NAN\00PM\00AM\00LC_ALL\00LANG\00INF\00g{Y0u_C\000123456789\00C.UTF-8\00.\00(null)\00Incorrect!\00Pure virtual function called!\00Correct!! Flag is here!!\00feag5gwea1411_efae!!\00libc++abi: \00Your UserName : \00Your PassWord : 
~~~
```
フラグの断片のようなものが見える。  
Leetになっていそうなものを拾うと、以下のようになる(フラグ形式が異なる点に注意)。  
```
3r!}
4n_3x
0us
p_0n_Br
3cut3_Cp
Fla
g{Y0u_C
```
意味が通るように組み合わせると`Flag{Y0u_C4n_3x3cut3_Cpp_0n_Br0us3r!}`となる。  
これがflagだった。  

## Flag{Y0u_C4n_3x3cut3_Cpp_0n_Br0us3r!}