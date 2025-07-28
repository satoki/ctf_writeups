# url-checker2:misc:100pts
有効なURLを作れますか？ Part2  
`nc url-checker2.challenges.beginners.seccon.jp 33458`  

[url-checker2.zip](url-checker2.zip)  

# Solution
[url-checker](../url-checker/)の続きのようだ。  
配布されたmain.pyは以下の通りであった。  
```py
from urllib.parse import urlparse

print(
    r"""
 _   _ ____  _        ____ _               _            ____  
| | | |  _ \| |      / ___| |__   ___  ___| | _____ _ _|___ \ 
| | | | |_) | |     | |   | '_ \ / _ \/ __| |/ / _ \ '__|__) |
| |_| |  _ <| |___  | |___| | | |  __/ (__|   <  __/ |  / __/ 
 \___/|_| \_\_____|  \____|_| |_|\___|\___|_|\_\___|_| |_____|
                                                              
allowed_hostname = "example.com"                                                         
>> """,
    end="",
)

allowed_hostname = "example.com"
user_input = input("Enter a URL: ").strip()
parsed = urlparse(user_input)

# Remove port if present
input_hostname = None
if ':' in parsed.netloc:
    input_hostname = parsed.netloc.split(':')[0]

try:
    if parsed.hostname == allowed_hostname:
        print("You entered the allowed URL :)")
    elif input_hostname and input_hostname == allowed_hostname and parsed.hostname and parsed.hostname.startswith(allowed_hostname):
        print(f"Valid URL :)")
        print("Flag: ctf4b{dummy_flag}")
    else:
        print(f"Invalid URL x_x, expected hostname {allowed_hostname}, got {parsed.hostname if parsed.hostname else 'None'}")
except Exception as e:
    print("Error happened")
```
受け取ったURLからポートを取り除いた`parsed.netloc.split(':')[0]`が`allowed_hostname`である場合にフラグが得られるようだ。  
ただし、`parsed.hostname`が`allowed_hostname`から始まっている必要もある。  
`http://example.com.satoki`のようなURLを指定したいが、`parsed.netloc`が`example.com`と一致するはずもない。  
ここで、`parsed.netloc`には`username:password@example.com.satoki`のように認証情報を付加できることに気づく。  
`example.com:password@example.com.satoki`とすると、ポートを取り除く手順で先頭の`example.com`より後ろが誤って取り除かれる。  
```bash
$ nc url-checker2.challenges.beginners.seccon.jp 33458

 _   _ ____  _        ____ _               _            ____
| | | |  _ \| |      / ___| |__   ___  ___| | _____ _ _|___ \
| | | | |_) | |     | |   | '_ \ / _ \/ __| |/ / _ \ '__|__) |
| |_| |  _ <| |___  | |___| | | |  __/ (__|   <  __/ |  / __/
 \___/|_| \_\_____|  \____|_| |_|\___|\___|_|\_\___|_| |_____|

allowed_hostname = "example.com"
>> Enter a URL: http://example.com:password@example.com.satoki
Valid URL :)
Flag: ctf4b{cu570m_pr0c3551n6_0f_url5_15_d4n63r0u5}
```
`http://example.com:password@example.com.satoki`でflagが表示された。  

## ctf4b{cu570m_pr0c3551n6_0f_url5_15_d4n63r0u5}