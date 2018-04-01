import json

import utils
from handler import Handler


class SetPermissionLevel(Handler):
    def handle(self, environ, start_response):
        c = utils.getCursor()
        permissionLevelString = utils.environToContents(environ)
        permissionLevelJson = json.loads(permissionLevelString)
        userId = permissionLevelJson['id']
        permissionLevel = permissionLevelJson['permissionLevel']
        if utils.checkUserPermissions(environ['user'], 3):
            c.execute("UPDATE users SET permissionLevel = ? WHERE id = ?", [permissionLevel, userId])

            c.execute("SELECT * FROM users WHERE permissionLevel = 3")
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
        return []

    def getHandled(self):
        return "setPermissionLevel"
