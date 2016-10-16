import json

import utils


def handleSessionDelete(request):
    c = utils.getCursor()

    sessionJsonString = request.rfile.read1(99999999).decode()
    sessionJson = json.loads(sessionJsonString)
    sessionId = sessionJson['sessionId']

    if not utils.checkUserPermissions(utils.getCurrentUser(request), 2):
        request.send_response(500)
        request.end_headers()
        request.wfile.write("Access Denied")
        return

    c.execute("delete from sessions where id = ?", [sessionId])
    c.connection.commit()
    c.connection.close()
    request.send_response(200)
    request.end_headers()
    return
