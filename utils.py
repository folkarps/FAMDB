import base64
import sqlite3
from datetime import datetime
from http import cookies

import psutil
from Crypto.Cipher import AES

sessionGenKey = str.encode(datetime.today().ctime())

__props = dict(line.strip().split('=') for line in open('config.config'))

missionMainDir = __props['missionMainDir']
missionMainArchive = __props['missionMainArchive']

missionMakerDir = __props['missionMakerDir']
missionMakerArchive = __props['missionMakerArchive']

port = int(__props['port'])


def getCursor():
    conn = sqlite3.connect('famdb.db', detect_types=sqlite3.PARSE_DECLTYPES)
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


def userToSessionId(user):
    return bytes.decode(
        base64.b64encode(AES.new(sessionGenKey).encrypt(user['id'].to_bytes(16, byteorder='little'))))


def getCurrentUser(request):
    C = cookies.SimpleCookie()
    C.load(request.headers["cookie"])
    if 'sessionId' not in C:
        return None
    sessionId = C['sessionId'].value

    userId = int.from_bytes(AES.new(sessionGenKey).decrypt(base64.b64decode(sessionId)), byteorder='little')

    if userId > 9223372036854775807:
        return None
    c = getCursor()
    c.execute('''select * from users where id = ?''', [userId])
    user = c.fetchone()
    if user is None:
        return None
    return User(user['email'], user['permissionLevel'], user['login'])


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
