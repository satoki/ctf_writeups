const express = require('express');
const mysql = require('mysql');
const session = require('express-session');
const bcrypt = require('bcrypt');
const fs = require('fs');

const MYSQL_HOST = process.env.MYSQL_HOST;
const MYSQL_USER = process.env.MYSQL_USER;
const MYSQL_PASSWORD = process.env.MYSQL_PASSWORD;
const MYSQL_DATABASE = process.env.MYSQL_DATABASE;
const SECRET = process.env.SECRET;

const connection = mysql.createConnection({
  host: MYSQL_HOST,
  user: MYSQL_USER,
  password: MYSQL_PASSWORD,
  database: MYSQL_DATABASE
});

const app = express();
app.use(express.json());
app.use(express.static('views'));

app.use(session({
  resave:true,
  saveUninitialized:true,
  secret:SECRET,
  cookie:{maxAge:3600000*24}
}));

app.get('',(req,res) => {
  return res.send('Welcome');
})


app.post('/login', (req, res) => {
  const { username, password } = req.body;
  connection.query('SELECT * FROM users WHERE username = ? LIMIT 1', [username], (err, rows) => {
    if (err) {
      return res.send({ error: err.message });
    }
    if (rows.length === 0) {
      return res.send({ error: 'Invalid username or password' });
    }
    
    const user = rows[0];
    bcrypt.compare(password, user.password, (err, result) => {
      if (err) {
        return res.send({ error: err.message });
      }
      if (!result) {
        return res.send({ error: 'Invalid username or password' });
      }
      
      const { id, username, is_admin } = user;
      req.session.loggedIn = true;
      req.session.user = { id, username, is_admin };
      res.send({ success: true, user: { id, username, is_admin } });
    });
  });
});

app.post('/register', (req, res) => {
  const { username, password, is_admin } = req.body;

  if (is_admin) {
    return res.send({ message: 'Hacking is not allowed. Please stop it.' });
  }

  const hashedPassword = bcrypt.hashSync(password, 10);
  connection.query('INSERT INTO users (username, password) VALUES (?, ?)', [username, hashedPassword], (err, result) => {
    if (err) {
      return res.send({ error: err.message });
    }
    const insertedUserId = result.insertId;
    connection.query('SELECT * FROM users WHERE id = ?', [insertedUserId], (err, rows) => {
      if (err) {
        return res.send({ error: err.message });
      }
      res.send(rows[0]);
    });
  });
});

app.post('/admin', (req, res) => {
  if (!req.session.loggedIn) {
    res.redirect('/?message=Please+login+first');
  } else {
    if (!req.session.user.is_admin) {
      return res.send({ error: 'You must be an admin to perform this action' });
    } else {
      const { id, is_admin } = req.body;
      connection.query('UPDATE users SET is_admin = ? WHERE id = ?', [is_admin, id], (err, result) => {
        if (err) {
          return res.send({ error: err.message });
        }
        const response = {
          success: true,
          affectedRows: result.affectedRows
        };
        res.send(response);
      });
    }
  }
});

app.get('/me', (req, res) => {
  if (!req.session.loggedIn) {
    res.redirect('/?message=Please+login+first');
  } else {
    if (!req.session.user.id) {
      return res.send({ error: 'User not found' });
    } else {
      const userId = req.session.user.id;
      connection.query('SELECT * FROM users WHERE id = ?', [userId], (err, rows) => {
        if (err) {
          return res.send({ error: err.message });
        }
        if (rows.length === 0) {
          return res.send({ error: 'User not found' });
        }
    
        res.send({
          user: {
            id: rows[0].id,
            username: rows[0].username,
            is_admin: rows[0].is_admin
          }
        });
      });
    }
  }
});

app.post('/profile', (req, res) => {
  if (!req.session.loggedIn) {
    res.redirect('/?message=Please+login+first');
  } else {
    if (!req.session.user.id) {
      return res.send({ error: 'You must be logged in to update your profile' });
    } else {
      const { username, password, is_admin = false } = req.body;
      let hashedPassword = null;
      if (password) {
        hashedPassword = bcrypt.hashSync(password, 10);
      }
      const userId = req.session.user.id;
      connection.query(
        'UPDATE users SET username = IFNULL(?, username), password = IFNULL(?, password), is_admin = IFNULL(?, is_admin) WHERE id = ?',
        [username, hashedPassword, is_admin, userId],
        (err, rows) => {
          if (err) {
            return res.send({ error: err.message });
          }
          req.session.user.username = username || req.session.user.username;
          res.send({ success: true });
        }
      );
    }
  }
});


app.post('/flag', (req, res) => {
  if (!req.session.loggedIn) {
    res.redirect('/?message=Please+login+first');
  } else {
    if (!req.session.user.is_admin) {
      return res.send({ error: 'You must be an admin to perform this action' });
    } else {
      fs.readFile('/flag', 'utf8', (err, data) => {
        if (err) {
          return res.send({ error: err.message });
        }
        res.send({ success: true, flag: data });
      });
    }
  }
});

app.get('/logout', (req, res) => {
  req.session.loggedIn = false;
  req.session.user = null;
  req.session.destroy((err) => {
    if (err) {
      return res.send({ error: err.message });
    }
    res.redirect('/');
  });
});

app.listen(3000, () => {
  console.log('Server listening on port 3000');
});