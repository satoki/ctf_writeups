global.__rootdir = __dirname;

const express = require('express');
const bodyParser = require('body-parser');
const cookieParser = require('cookie-parser');
const path = require('path');
const crypto = require('crypto');

require('dotenv').config();

const INTEGRITY = '12370cc0f387730fb3f273e4d46a94e5';

const app = express();

app.use(bodyParser.json({ extended: false }));
app.use(cookieParser());

app.post('/api/login', async (req, res) => {
    if (!req.body.username || typeof req.body.username !== 'string') {
        res.status(400);
        res.end();
        return;
    }
    res.json({'token': await generateToken(req.body.username)});
    res.end;
});

app.get('/api/validate', async (req, res) => {
    if (!req.cookies.token || typeof req.cookies.token !== 'string') {
        res.json({success: false, error: 'Invalid token'});
        res.end();
        return;
    }

    const result = await decodeToken(req.cookies.token);
    if (!result) {
        res.json({success: false, error: 'Invalid token'});
        res.end();
        return;
    }

    res.json({success: true, token: result});
});

app.get('/api/flag', async (req, res) => {
    if (!req.cookies.token || typeof req.cookies.token !== 'string') {
        res.json({success: false, error: 'Invalid token'});
        res.end();
        return;
    }

    const result = await decodeToken(req.cookies.token);
    if (!result) {
        res.json({success: false, error: 'Invalid token'});
        res.end();
        return;
    }

    if (!result.member) {
        res.json({success: false, error: 'You are not a member'});
        res.end();
        return;
    }

    res.json({success: true, flag: process.env.FLAG});
});

app.use(express.static(path.join(__dirname, '/public')));

app.listen(process.env.PORT || 3000);

async function generateToken(username) {
    const algorithm = 'aes-192-cbc'; 
    const key = Buffer.from(process.env.KEY, 'hex'); 
    // Predictable IV doesn't matter here
    const iv = Buffer.alloc(16, 0);

    const cipher = crypto.createCipheriv(algorithm, key, iv);

    const token = `{"integrity":"${INTEGRITY}","member":0,"username":"${username}"}`

    let encrypted = '';
    encrypted += cipher.update(token, 'utf8', 'base64');
    encrypted += cipher.final('base64');
    return encrypted;
}

async function decodeToken(encrypted) {
    const algorithm = 'aes-192-cbc'; 
    const key = Buffer.from(process.env.KEY, 'hex'); 
    // Predictable IV doesn't matter here
    const iv = Buffer.alloc(16, 0);
    const decipher = crypto.createDecipheriv(algorithm, key, iv);

    let decrypted = '';

    try {
        decrypted += decipher.update(encrypted, 'base64', 'utf8');
        decrypted += decipher.final('utf8');
    } catch (error) {
        return false;
    }

    let res;
    try {
        res = JSON.parse(decrypted);
    } catch (error) {
        console.log(error);
        return false;
    }

    if (res.integrity !== INTEGRITY) {
        return false;
    }

    return res;
}
