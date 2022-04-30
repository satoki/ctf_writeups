# To Be And Not To Be:Miscellaneous:261pts
To be and not to be, that is the question. (Note: the correct input solution to this challenge is alphanumeric.)  

**Connect with:**  
```
nc challenge.nahamcon.com 32518
```

# Solution
接続先が与えられるのでnetcatで繋ぐと以下のようであった。  
```bash
$ nc challenge.nahamcon.com 32518
we've got a funky shell over here, and we're going to feed it your input!
the shell will run the following:
console.log(%s !== (%s));
And the flag is `flag{<md5>}, where <md5> is the md5sum of the input that prints true!
>>>A
yeah that's gonna be a no from me dog
>>>aaaaa
way too much or bad dater...
>>>0
Nope!
```
`console.log(%s !== (%s));`をtrueにすればよいようだ。  
JavaScriptには`NaN`なるものがあり、これらの厳密な比較はfalseとなる。  
```bash
$ node
~~~
> 1 === 1
true
> NaN === NaN
false
> NaN !== NaN
true
```
`NaN`が答えのようだ。  
```bash
$ nc challenge.nahamcon.com 32518
we've got a funky shell over here, and we're going to feed it your input!
the shell will run the following:
console.log(%s !== (%s));
And the flag is `flag{<md5>}, where <md5> is the md5sum of the input that prints true!
>>>NaN
Congrats!

$ echo -n 'NaN' | md5sum
7ecfb3bf076a6a9635f975fe96ac97fd  -
```
ハッシュを指定された形式にするとflagとなった。  

## flag{7ecfb3bf076a6a9635f975fe96ac97fd}