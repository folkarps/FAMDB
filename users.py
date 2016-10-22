import json

import utils


def handleUsers(environ, start_response):
    user = environ['user']
    c = utils.getCursor()
    c.execute("select id, login, permissionLevel, lastLogin, email from users")
    allUsers = c.fetchall()

    userDtos = [dict(x) for x in allUsers]

    if user is None:
        start_response("403 Permission Denied", [])
        return ["Access Denied"]

    if user is not None and user.permissionLevel > 2:
        for x in userDtos:
            x['permissionLevels'] = [x['permissionLevel']] + [-1, 0, 1, 2, 3]
    else:
        for x in userDtos:
            x['permissionLevels'] = x['permissionLevel']

    encode = json.dumps(userDtos).encode()
    start_response("200 OK", [])
    return [encode]
