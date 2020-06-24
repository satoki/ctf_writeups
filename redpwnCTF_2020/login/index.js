global.__rootdir = __dirname;

const express = require('express');
const bodyParser = require('body-parser');
const cookieParser = require('cookie-parser');
const path = require('path');
const db = require('better-sqlite3')('db.sqlite3');

require('dotenv').config();

const app = express();

app.use(bodyParser.json({ extended: false }));
app.use(cookieParser());

app.post('/api/flag', (req, res) => {
    const username = req.body.username;
    const password = req.body.password;
    if (typeof username !== 'string') {
        res.status(400);
        res.end();
        return;
    }
    if (typeof password !== 'string') {
        res.status(400);
        res.end();
        return;
    }

    let result;
    try {
        result = db.prepare(`SELECT * FROM users 
            WHERE username = '${username}'
            AND password = '${password}';`).get();
    } catch (error) {
        res.json({ success: false, error: "There was a problem." });
        res.end();
        return;
    }
    
    if (result) {
        res.json({ success: true, flag: process.env.FLAG });
        res.end();
        return;
    }

    res.json({ success: false, error: "Incorrect username or password." });
});

app.use(express.static(path.join(__dirname, '/public')));

app.listen(process.env.PORT || 3000);

// init database
db.prepare(`CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT);`).run();

db.prepare(`INSERT INTO 
    users (username, password)
    VALUES ('${process.env.USERNAME}', '${process.env.PASSWORD}');`).run();
