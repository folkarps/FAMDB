import json

import utils


def handlePermissionLevel(request):
    c = utils.getCursor()
    permissionLevelString = request.rfile.read1(99999999).decode()
    permissionLevelJson = json.loads(permissionLevelString)
    userId = permissionLevelJson['id']
    permissionLevel = permissionLevelJson['permissionLevel']
    if utils.checkUserPermissions(utils.getCurrentUser(request), 3):
        c.execute("update users set permissionLevel = ? where id = ?", [permissionLevel, userId])

        c.execute("select * from users where permissionLevel = 3")
        if c.fetchone() is None:
            request.send_response(500)
            request.end_headers()
            request.wfile.write("No admin users found, there must be at least one high admin (3)".encode())
        else:
            request.send_response(200)
            request.end_headers()
            c.connection.commit()
            c.connection.close()
    else:
        request.send_response(500)
        request.end_headers()
        request.wfile.write("access denied".encode())
