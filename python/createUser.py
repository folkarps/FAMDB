import sqlite3
from datetime import date
from http import cookies

from passlib.hash import sha256_crypt


def handleCreateUser(request):
    conn = sqlite3.connect('famdb.db', detect_types=sqlite3.PARSE_DECLTYPES)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    login = request.rfile.readline()
    email = request.rfile.readline()
    passw = request.rfile.readline()
    c.execute('''select * from users where login = ?''', [login])
    if c.fetchone() is None:
        c.execute('''insert into users (login, password, email, lastLogin, permissionLevel) values (?, ?, ?, ?)''',
                  [login, sha256_crypt.encrypt(passw), email, date.today(), 0])
        c.execute('''select * from users where login = ?''', [login])
        user = c.fetchone()
        cookie = cookies.SimpleCookie()
        cookie['sessionId'] = user['id']
        request.send_header(cookie.output())
    return
