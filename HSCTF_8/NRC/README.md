# NRC:web:107pts
Find the flag :)  
[no-right-click.hsc.tf](https://no-right-click.hsc.tf/)  

# Solution
アクセスすると右クリックが禁止されているようだ。  
Document  
[site.png](site/site.png)  
FirefoxではShiftを押しながらであれば右クリック可能となる。  
ソースを漁ると、useless-file.cssにflagが書かれていた。  
```css:useless-file.css
body {
    text-align: center;
    font-size: 5rem;
    font-family: 'Abril Fatface', cursive;
}

.small {
    margin-top: 50vh;
    font-size: 0.5rem;
}

/* cause i disabled it in index.js */
/* no right click = n.r.c. */
/* flag{keyboard_shortcuts_or_taskbar} */
```

## flag{keyboard_shortcuts_or_taskbar}