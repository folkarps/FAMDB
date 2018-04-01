import html
import json
from datetime import date

import utils
from handler import Handler


class SaveMissionHandler(Handler):
    def handle(self, environ, start_response):
        c = utils.getCursor()
        missionJsonString = utils.environToContents(environ)
        missionJson = json.loads(missionJsonString)
        # create a blank row, then update that row so that we don't have 2 different statements
        if 'missionId' not in missionJson:
            c.execute("INSERT INTO missions (missionName) VALUES (?)", [missionJson['missionName']])
            c.execute("SELECT max(id) FROM missions")
            missionId = c.fetchone()[0]
            newMission = True
            hasPermissions = utils.checkUserPermissions(environ['user'], 0)
        else:
            newMission = False
            missionId = missionJson['missionId']
            c.execute("SELECT * FROM missions WHERE id = ?", [missionId])
            mission = c.fetchone()
            if mission is None:
                start_response("500 Internal Server Response", [])
                return ["Stop trying to edit a mission that doesn't exist".encode()]
            hasPermissions = utils.checkUserPermissions(environ['user'], 2, missionId)

        if not hasPermissions:
            start_response("403 Permission Denied", [])
            return ["Access Denied"]
        query, params = SaveMissionHandler.constructQuery(missionJson, newMission, environ['user'])
        params.append(missionId)

        c.execute("update missions set " + query + "where id=?", params)
        c.connection.commit()
        c.connection.close()
        start_response("201 Created", [])
        return [(str(missionId)).encode()]

    def getHandled(self):
        return "saveMission"

    def constructQuery(self, missionJson, newMission, user):
        queryParts = []
        params = []

        for part in ['missionPlayers', 'missionMap', 'missionType', 'missionDesc', 'missionNotes',
                     'framework', 'missionName']:
            queryParts.append(part + "=?")
            if missionJson[part] is str:
                params.append(html.escape(missionJson[part]))
            else:
                params.append(missionJson[part])

        queryParts.append("missionModified=?")
        params.append(date.today())
        if newMission:
            queryParts.append("missionAuthor=?")
            params.append(user.login)
        return " , ".join(queryParts), params
