import html
import json
import re
from datetime import date
from http import cookies

import requests
from Crypto.Cipher import AES
from passlib.hash import sha256_crypt

import utils


def handleCreateUser(environ, start_response):
    c = utils.getCursor()
    loginJsonString = utils.environToContents(environ)
    signUpJson = json.loads(loginJsonString)
    login = html.escape(signUpJson['login'].strip())
    email = html.escape(signUpJson['email'].strip())
    discordId = signUpJson['discordId'].strip()

    negativeRegex = re.compile(r'[0-9]{16}')
    if not negativeRegex.match(discordId):
        start_response("500 Internal Server Error", [])
        return ["Discord ID required."
                " <a href='https://support.discordapp.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-'>"
                " See This</a>".encode()]

    passw = signUpJson['password']
    c.execute('''select * from users where login = ? or email = ?''', [login, email])
    if login == '':
        start_response("500 Internal Server Error", [])
        return ["Did you think you were funny making a blank user name?".encode()]
    if email == '':
        start_response("500 Internal Server Error", [])
        return ["Did you think you were funny making a blank email?".encode()]
    if passw == '':
        start_response("500 Internal Server Error", [])
        return ["Did you think you were funny making a blank password?".encode()]
    if c.fetchone() is None:
        from Crypto import Random
        sessionKey = Random.new().read(AES.block_size)
        c.execute(
            '''insert into users (login, password, email, lastLogin, permissionLevel, sessionKey, discordId) values (?, ?, ?, ?, ?, ?, ?)''',
            [login, sha256_crypt.encrypt(passw), email, date.today(), 0, sessionKey, discordId])
        c.execute('''select * from users where login = ?''', [login])
        user = c.fetchone()
        if user['id'] == 1:
            c.execute("update users set permissionLevel = 3 where id = 1")
        cookie = cookies.SimpleCookie()
        cookie['famdbSessionId'] = utils.userRowToSessionId(user)
        header1 = ('set-cookie', cookie.output(header=''))
        cookie = cookies.SimpleCookie()
        cookie['permissionLevel'] = user['permissionLevel']
        header2 = ('set-cookie', cookie.output(header=''))
        start_response("200 OK", [header1, header2])
        c.connection.commit()
        c.connection.close()

        if utils.discordHookUrl != '':
            payload = {
                'content': 'Comrades! Welcome our new mission maker  <@' + discordId
                           + '>. Hopefully they add will a great many missions to our cause!'}

            r = requests.post(utils.discordHookUrl, data=payload)
        return []
    else:
        start_response("500 Internal Server Error", [])
        return ["user with that login or email already exists".encode()]
