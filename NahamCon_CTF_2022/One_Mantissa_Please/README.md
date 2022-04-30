# One Mantissa Please:Miscellaneous:276pts
I'll have one mantissa to go, please! (Note: the correct answer is the smallest positive integer value.)  

**Connect with:**  
```
nc challenge.nahamcon.com 31337
```

# Solution
接続先が与えられるのでnetcatで繋ぐと以下のようであった。  
```bash
$ nc challenge.nahamcon.com 31337
we've got a funky shell over here, and we're going to feed it your input!
the shell will run the following:
console.log(%d == (%d + 1));
And the flag is `flag{<md5>}, where <md5> is the md5sum of the smallest integer input that prints true!
>>>1
Nope!
>>>
```
`console.log(%d == (%d + 1));`がtrueになる最小の数のmd5がフラグのようだ。  
JavaScriptなのでintのMAXあたりが怪しく、+1しても厳密な等価でない場合に同値となったことを思い出す。  
```bash
$ node
~~~
> Number.MAX_SAFE_INTEGER
9007199254740991
> Number.MAX_SAFE_INTEGER == Number.MAX_SAFE_INTEGER+1
false
> Number.MAX_SAFE_INTEGER+1 == Number.MAX_SAFE_INTEGER+2
true
> Number.MAX_SAFE_INTEGER+1
9007199254740992
```
`9007199254740992`でよいと分かった。  
```bash
$ nc challenge.nahamcon.com 31337
we've got a funky shell over here, and we're going to feed it your input!
the shell will run the following:
console.log(%d == (%d + 1));
And the flag is `flag{<md5>}, where <md5> is the md5sum of the smallest integer input that prints true!
>>>9007199254740992
Congrats!

$ echo -n '9007199254740992' | md5sum
3a78300a68de2a1210c9e3726c3cb87a  -
```
ハッシュを指定された形式にするとflagとなった。  

## flag{3a78300a68de2a1210c9e3726c3cb87a}