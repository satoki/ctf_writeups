from flask import Flask, request, make_response

app = Flask(__name__)

UUID_12 = "bc079f55-f1ac-4228-8d60-ce4b4ff93396/bf56333b-0f6b-46a6-beec-3cfb72253c55"

@app.route("/", methods=["GET", "OPTIONS"])
def index():

    def add_cors_headers(resp):
        resp.headers["Access-Control-Allow-Origin"] = "*"
        resp.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS"
        resp.headers["Access-Control-Allow-Headers"] = "*"
        return resp

    if request.method == "OPTIONS":
        resp = make_response()
        return add_cors_headers(resp)

    resp = make_response(f"file:///tmp/{UUID_12}/index.html")
    return add_cors_headers(resp)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)