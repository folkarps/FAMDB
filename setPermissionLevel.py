import json

import utils


def handlePermissionLevel(environ, start_response):
    c = utils.getCursor()
    permissionLevelString = utils.environToContents(environ)
    permissionLevelJson = json.loads(permissionLevelString)
    userId = permissionLevelJson['id']
    permissionLevel = permissionLevelJson['permissionLevel']
    if utils.checkUserPermissions(environ['user'], 3):
        c.execute("update users set permissionLevel = ? where id = ?", [permissionLevel, userId])

        c.execute("select * from users where permissionLevel = 3")
        if c.fetchone() is None:
            start_response("500 Internal Server Error", [])
            return ["No admin users found, there must be at least one high admin (3)".encode()]
        else:
            start_response("200 OK", [])
            c.connection.commit()
            c.connection.close()
    else:
        start_response("403 Permission Denied", [])
        return ["Access Denied".encode()]
