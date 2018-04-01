import json

import utils
from handler import Handler


class DeleteSessionHandler(Handler):
    def handle(self, environ, start_response):
        c = utils.getCursor()
        sessionJsonString = utils.environToContents(environ)
        sessionJson = json.loads(sessionJsonString)
        sessionId = sessionJson['sessionId']

        if not utils.checkUserPermissions(environ['user'], 2):
            start_response("403 Permission Denied", [])
            return ["Access Denied"]

        c.execute("DELETE FROM sessions WHERE id = ?", [sessionId])
        c.connection.commit()
        c.connection.close()
        start_response("200 OK", [])
        return []

    def getHandled(self):
        return "deleteSession"
