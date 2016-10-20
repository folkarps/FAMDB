import json

import utils


def handleUsers(request):
    user = utils.getCurrentUser(request)
    c = utils.getCursor()
    c.execute("select id, login, permissionLevel, lastLogin, email from users")
    allUsers = c.fetchall()

    userDtos = [dict(x) for x in allUsers]

    if user is None or user.permissionLevel < 1:
        request.wfile.write("".encode())
        return

    if user is not None and user.permissionLevel > 2:
        for x in userDtos:
            x['permissionLevels'] = [x['permissionLevel']] + [-1, 0, 1, 2, 3]
    else:
        for x in userDtos:
            x['permissionLevels'] = x['permissionLevel']

    encode = json.dumps(userDtos).encode()
    request.wfile.write(encode)
    return
