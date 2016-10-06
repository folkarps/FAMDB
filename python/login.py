import base64
import sqlite3
from datetime import date
from http import cookies

from Crypto.Cipher import AES
from passlib.hash import sha256_crypt

import utils


def handleLogin(request):
    conn = sqlite3.connect('famdb.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    login = request.rfile.readline().decode().replace("\n", "")
    passw = request.rfile.readline().decode().replace("\n", "")
    c.execute('''select * from users where login = ?''', [login])
    user = c.fetchone()
    if user is None:
        request.wfile.write("No user with this login")
    if sha256_crypt.verify(passw, user['password']):
        cookie = cookies.SimpleCookie()
        cookie['sessionId'] = bytes.decode(
            base64.b64encode(AES.new(utils.sessionGenKey).encrypt(user['id'].to_bytes(16, byteorder='big'))))
        request.send_response(200)
        request.send_header('set-cookie', cookie.output(header=''))
        request.end_headers()
        c.execute("update users set lastLogin = ?", [date.today()])
        conn.commit()
        conn.close()
    else:
        request.wfile.write("incorrect password")
    return
