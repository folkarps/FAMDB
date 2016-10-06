import sqlite3
from datetime import date
from http import cookies

from Crypto.Cipher import AES
from passlib.hash import sha256_crypt

import utils


def handleLogon(request):
    conn = sqlite3.connect('famdb.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    login = request.rfile.readline()
    passw = request.rfile.readline()
    c.execute('''select * from users where login = ?''', [login])
    user = c.fetchone()
    if sha256_crypt.verify(passw, user['password']):
        cookie = cookies.SimpleCookie()
        cookie['sessionId'] = AES.new(utils.sessionGenKey).encrypt(user['id'])
        request.send_header(cookie.output())
        c.execute("update users set lastLogin = ?", [date.today()])
    return
