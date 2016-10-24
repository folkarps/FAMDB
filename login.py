import json
from datetime import date
from http import cookies

from passlib.hash import sha256_crypt

import utils


def handleLogin(environ, start_response):
    c = utils.getCursor()
    loginJsonString = utils.environToContents(environ)
    loginJson = json.loads(loginJsonString)
    login = loginJson['login']
    passw = loginJson['password']
    c.execute('''select * from users where login = ?''', [login])
    user = c.fetchone()
    if user is None:
        start_response("500 Internal Server Response", [])
        return ["No user with this login".encode()]
    if sha256_crypt.verify(passw, user['password']):
        cookie = cookies.SimpleCookie()
        cookie['famdbSessionId'] = utils.userRowToSessionId(user)
        header1 = ('set-cookie', cookie.output(header=''))
        cookie = cookies.SimpleCookie()
        cookie['permissionLevel'] = user['permissionLevel']
        header2 = ('set-cookie', cookie.output(header=''))
        print("returning to user:" + utils.userRowToSessionId(user))
        start_response("200 OK", [header1, header2])
        c.execute("update users set lastLogin = ?", [date.today()])
        c.connection.commit()
        c.connection.close()
    else:
        return ["incorrect password".encode()]
    return []
