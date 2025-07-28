# url-checker:misc:100pts
有効なURLを作れますか？  
`nc url-checker.challenges.beginners.seccon.jp 33457`  

[url-checker.zip](url-checker.zip)  

# Solution
接続先とソースコードが渡される。  
配布されたmain.pyは以下の通りであった。  
```py
from urllib.parse import urlparse

print(
    r"""
 _   _ ____  _        ____ _               _             
| | | |  _ \| |      / ___| |__   ___  ___| | _____ _ __ 
| | | | |_) | |     | |   | '_ \ / _ \/ __| |/ / _ \ '__|
| |_| |  _ <| |___  | |___| | | |  __/ (__|   <  __/ |   
 \___/|_| \_\_____|  \____|_| |_|\___|\___|_|\_\___|_|   

allowed_hostname = "example.com"                                                         
>> """,
    end="",
)

allowed_hostname = "example.com"
user_input = input("Enter a URL: ").strip()
parsed = urlparse(user_input)

try:
    if parsed.hostname == allowed_hostname:
        print("You entered the allowed URL :)")
    elif parsed.hostname and parsed.hostname.startswith(allowed_hostname):
        print(f"Valid URL :)")
        print("Flag: ctf4b{dummy_flag}")
    else:
        print(f"Invalid URL x_x, expected hostname {allowed_hostname}, got {parsed.hostname if parsed.hostname else 'None'}")
except Exception as e:
    print("Error happened")
```
URLを受け取るようで、`allowed_hostname`として`example.com`が指定されている。  
`parsed.hostname`が`allowed_hostname`とは完全一致しないが、`allowed_hostname`で始まっている場合にフラグが得られるようだ。  
```bash
$ nc url-checker.challenges.beginners.seccon.jp 33457

 _   _ ____  _        ____ _               _
| | | |  _ \| |      / ___| |__   ___  ___| | _____ _ __
| | | | |_) | |     | |   | '_ \ / _ \/ __| |/ / _ \ '__|
| |_| |  _ <| |___  | |___| | | |  __/ (__|   <  __/ |
 \___/|_| \_\_____|  \____|_| |_|\___|\___|_|\_\___|_|

allowed_hostname = "example.com"
>> Enter a URL: http://example.com.satoki
Valid URL :)
Flag: ctf4b{574r75w17h_50m371m35_n07_53cur37}
```
`http://example.com.satoki`でflagが表示された。  

## ctf4b{574r75w17h_50m371m35_n07_53cur37}