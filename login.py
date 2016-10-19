import json
from datetime import date
from http import cookies

from passlib.hash import sha256_crypt

import utils


def handleLogin(request):
    c = utils.getCursor()
    loginJsonString = request.rfile.read1(99999999).decode()
    loginJson = json.loads(loginJsonString)
    login = loginJson['login']
    passw = loginJson['password']
    c.execute('''select * from users where login = ?''', [login])
    user = c.fetchone()
    if user is None:
        request.wfile.write("No user with this login".encode())
        return
    if sha256_crypt.verify(passw, user['password']):
        cookie = cookies.SimpleCookie()
        cookie['sessionId'] = utils.userRowToSessionId(user)
        request.send_response(200)
        request.send_header('set-cookie', cookie.output(header=''))
        cookie = cookies.SimpleCookie()
        cookie['permissionLevel'] = user['permissionLevel']
        request.send_header('set-cookie', cookie.output(header=''))
        request.end_headers()
        c.execute("update users set lastLogin = ?", [date.today()])
        c.connection.commit()
        c.connection.close()
    else:
        request.wfile.write("incorrect password".encode())
    return
