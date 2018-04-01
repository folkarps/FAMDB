import json

import utils
from handler import Handler


class DeleteMissionHandler(Handler):
    def handle(self, environ, start_response):
        c = utils.getCursor()

        missionJsonString = utils.environToContents(environ)
        missionJson = json.loads(missionJsonString)
        missionId = missionJson['missionId']

        # if you're a low admin or this is your mission
        if not utils.checkUserPermissions(environ['user'], 2, missionId):
            start_response("403 Permission Denied", [])
            return ["Access Denied"]

        c.execute("DELETE FROM versions WHERE missionId = ?", [missionId])
        c.execute("DELETE FROM missions WHERE id = ?", [missionId])
        c.connection.commit()
        c.connection.close()
        start_response("200 OK", [])
        return []

    def getHandled(self):
        return "deleteMission"
