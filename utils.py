import base64
import os
import sqlite3
from http.cookies import SimpleCookie

import psutil

currentPath = os.path.dirname(os.path.realpath(__file__))
__props = dict(line.strip().split('=') for line in open(currentPath + '/config.config'))

missionMainDir = __props['missionMainDir']
missionMainArchive = __props['missionMainArchive']

missionMakerDir = __props['missionMakerDir']
missionMakerArchive = __props['missionMakerArchive']

port = int(__props['port'])


def getCursor():
    conn = sqlite3.connect(currentPath + '/famdb.db', detect_types=sqlite3.PARSE_DECLTYPES)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    return c


# 0 = new user
# 1 = trusted MM
# 2 = low admin (full mission rights)
# 3 = high admin (full rights)
class User:
    def __init__(self, email, permissionLevel, login):
        self.email = email
        self.permissionLevel = permissionLevel
        self.login = login


def userRowToSessionId(user):
    return base64.b64encode(user['sessionKey']).decode()


def getCurrentUser(cookie):
    if 'famdbSessionId' not in cookie:
        return None
    sessionId = cookie['famdbSessionId'].value

    try:
        decode = base64.b64decode(sessionId)
        c = getCursor()
        c.execute('''select * from users where sessionKey = ?''', [decode])
        user = c.fetchone()
        if user is None:
            return None
        return User(user['email'], user['permissionLevel'], user['login'])
    except Exception as exc:
        print("error getting current User: {0}".format(exc))
        return None


def environToContents(environ):
    try:
        length = int(environ.get('CONTENT_LENGTH', '0'))
    except ValueError:
        length = 0
    if length != 0:
        return environ['wsgi.input'].read(length).decode()
    return ""


def AND(one: bool, two: bool):
    return one and two


def OR(one: bool, two: bool):
    return one or two


def checkUserPermissions(user: User, requiredPermissionLevel=-1, missionId=None, collector=OR):
    authorMatch = False
    if user is None:
        return False
    if missionId is not None:
        c = getCursor()
        c.execute("select * from missions where id = ?", [missionId])
        mission = c.fetchone()
        if mission is None or user.permissionLevel < 0:
            authorMatch = False
        else:
            authorMatch = user.login in mission['missionAuthor']
    return collector(user.permissionLevel >= requiredPermissionLevel, authorMatch)


def isPidRunning(pid):
    try:
        p = psutil.Process(pid)
    except psutil.NoSuchProcess:
        return False
    else:
        return True


def handleBadSessionIds(environ):
    if environ['user'] is None and "HTTP_COOKIE" in environ:
        cookie = SimpleCookie(environ['HTTP_COOKIE'])
        if 'famdbSessionId' in cookie:
            return [('Set-Cookie', 'famdbSessionId=;expires=Thu, 01 Jan 1970 00:00:00 GMT;MaxAge=-1')]
        return []
    else:
        return []
