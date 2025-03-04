# Beginner's Flag Printer:Rev:100pts
フラグを出力するアセンブリです🤖  
```
.LC0:
        .string "Alpaca{%x}\n"
main:
        push    rbp
        mov     rbp, rsp
        sub     rsp, 16
        mov     DWORD PTR [rbp-4], 539232261
        mov     eax, DWORD PTR [rbp-4]
        mov     esi, eax
        mov     edi, OFFSET FLAT:.LC0
        mov     eax, 0
        call    printf
        mov     eax, 0
        leave
        ret
```

# Solution
アセンブリを読むとprintfの第一引数ediに`"Alpaca{%x}\n"`が、第二引数esiに`539232261`が入っていることがわかる。  
%xでHex表示されるため、539232261は20240805となる。  
AlpacaHackのスタート日のようだ。  

## Alpaca{20240805}