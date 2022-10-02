from bottle import route, run, response

@route("/")
def index():
    session = {"name": "admin"}
    response.set_cookie("name", session, secret="Se3333KKKKKKAAAAIIIIILLLLovVVVVV3333YYYYoooouuu")
    return "Satoki"

if __name__ == "__main__":
    run(host="0.0.0.0", port=8081)