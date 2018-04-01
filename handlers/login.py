import json
from datetime import date
from http import cookies

from passlib.hash import sha256_crypt

import utils
from handler import Handler


class LoginHandler(Handler):
    def handle(self, environ, start_response):
        c = utils.getCursor()
        loginJsonString = utils.environToContents(environ)
        loginJson = json.loads(loginJsonString)
        login = loginJson['login'].strip()
        passw = loginJson['password']
        c.execute('''SELECT * FROM users WHERE login = ?''', [login])
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
            start_response("200 OK", [header1, header2])
            c.execute("UPDATE users SET lastLogin = ?", [date.today()])
            c.connection.commit()
            c.connection.close()
        else:
            start_response("500 Internal Server Response", [])
            return ["incorrect password".encode()]
        return []

    def getHandled(self):
        return "login"
