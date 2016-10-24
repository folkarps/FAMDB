import json

import utils


def handleSessionDelete(environ, start_response):
    c = utils.getCursor()

    sessionJsonString = utils.environToContents(environ)
    sessionJson = json.loads(sessionJsonString)
    sessionId = sessionJson['sessionId']

    if not utils.checkUserPermissions(environ['user'], 2):
        start_response("403 Permission Denied", [])
        return ["Access Denied"]

    c.execute("delete from sessions where id = ?", [sessionId])
    c.connection.commit()
    c.connection.close()
    start_response("200 OK", [])
    return []
