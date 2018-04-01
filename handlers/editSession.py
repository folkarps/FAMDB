import json

import utils
from handler import Handler


class EditSessionHandler(Handler):
    def handle(self, environ, start_response):
        c = utils.getCursor()
        editSessionString = utils.environToContents(environ)
        editSessionJson = json.loads(editSessionString)
        sessionDate = editSessionJson['date']

        # if you're a low admin
        if not utils.checkUserPermissions(environ['user'], 2):
            start_response("403 Permission Denied", [])
            return ["Access Denied".encode()]

        if 'id' not in editSessionJson:
            c.execute("INSERT INTO sessions (date) VALUES (?)", [sessionDate])
            c.execute("SELECT max(id) FROM sessions")
            sessionId = c.fetchone()[0]
        else:
            sessionId = editSessionJson['id']

        c.execute("SELECT missionNames FROM sessions WHERE id = ?", [sessionId])
        existingMissionNames = c.fetchone()

        c.execute("UPDATE sessions SET missionNames = ?, host = ?, name = ?, players = ?, date = ? WHERE id = ? ",
                  EditSessionHandler.toParams(self, editSessionJson, sessionId))
        missions = editSessionJson['missionNames']

        newMissions = []

        if existingMissionNames['missionNames'] is not None:
            existingMissionNames = existingMissionNames['missionNames'].split(",")
            for mission in missions:
                if mission in existingMissionNames:
                    existingMissionNames.remove(mission)
                else:
                    newMissions.append(mission)
        else:
            newMissions = missions

        for mission in newMissions:
            c.execute("UPDATE missions SET playedCounter = playedCounter+1, lastPlayed=? WHERE missionName =?",
                      [sessionDate, mission])
        c.connection.commit()
        c.connection.close()
        start_response("201 Created", [])
        return [("location:" + str(sessionId)).encode()]

    def toParams(self, editSessionJson, sessionId):
        params = []
        params.append(",".join(editSessionJson['missionNames']))
        params.append(editSessionJson['host'])
        params.append(editSessionJson['name'])
        params.append(editSessionJson['players'])
        params.append(editSessionJson['date'])
        params.append(sessionId)
        return params

    def getHandled(self):
        return "editSession"
