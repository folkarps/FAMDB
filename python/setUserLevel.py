import json

import utils


def handleSetUserLevel(request):
    c = utils.getCursor()
    userJsonString = request.rfile.read1(99999999).decode()
    userJson = json.loads(userJsonString)
    if not utils.checkUserPermissions(utils.getCurrentUser(request), 3):
        request.wfile.write("Access denied".encode())
        return
    userId = userJson['id']
    level = userJson['level']
    c.execute("update users set permissionLevel = ? where id = ?", [level, userId])
    return
