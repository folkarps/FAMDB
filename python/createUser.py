import json
import sqlite3
from datetime import date
from http import cookies

from passlib.hash import sha256_crypt

import utils


def handleCreateUser(request):
    conn = sqlite3.connect('famdb.db', detect_types=sqlite3.PARSE_DECLTYPES)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    loginJsonString = request.rfile.read1(99999999).decode()
    signUpJson = json.loads(loginJsonString)
    login = signUpJson['login']
    email = signUpJson['email']
    passw = signUpJson['password']
    c.execute('''select * from users where login = ? or email = ?''', [login, email])
    if c.fetchone() is None:
        c.execute('''insert into users (login, password, email, lastLogin, permissionLevel) values (?, ?, ?, ?, ?)''',
                  [login, sha256_crypt.encrypt(passw), email, date.today(), 0])
        c.execute('''select * from users where login = ?''', [login])
        user = c.fetchone()
        cookie = cookies.SimpleCookie()
        cookie['sessionId'] = utils.userToSessionId(user)
        request.send_response(200)
        # python has horrible cookie management
        request.send_header('set-cookie', cookie.output(header=''))
        request.end_headers()
        conn.commit()
        conn.close()
    else:
        request.wfile.write("user with that login or email already exists".encode())
    return
