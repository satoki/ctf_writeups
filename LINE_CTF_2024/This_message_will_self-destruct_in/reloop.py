import time
from flask import Flask, redirect

app = Flask(__name__)

@app.route("/")
def infinite_redirect():
    time.sleep(2)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=80)