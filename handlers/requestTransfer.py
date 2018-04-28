import json
from pathlib import Path

import requests

import utils
from handler import Handler


class RequestTransferHandler(Handler):
    def handle(self, environ, start_response):
        user = environ['user']
        missionJsonString = utils.environToContents(environ)
        missionJson = json.loads(missionJsonString)
        missionId = missionJson['missionId']
        versionId = missionJson['versionId']
        # If you're a MM user and this is your mission, or you're a low admin
        if not utils.checkUserPermissions(environ['user'], 1, missionId):
            start_response("403 Permission Denied", [])
            return ["Access Denied"]

        c = utils.getCursor()
        c.execute("SELECT name FROM versions WHERE id = ?", [versionId])

        version = c.fetchone()
        fileName = version[0]
        if Path(utils.missionMakerDir + "/" + fileName).is_file():
            c.execute("UPDATE missions SET status='Transfer' WHERE id = ?", [missionId])
            c.execute("UPDATE versions SET requestedTransfer=1 WHERE id = ?", [versionId])

        if utils.discordHookUrl != '':
            c.execute("SELECT missionName, missionAuthor FROM missions WHERE id = ?", [missionId])
            missionStuff = c.fetchone()
            missionName = missionStuff[0]
            missionAuthor = missionStuff[1]

            payload = {'content': '<@&' + utils.discordAdminRoleId + '> Rejoice Comrades! ' + missionAuthor
                                  + ' has prepared a new adventure for us!\n' +
                                  missionName + ' now has ' + fileName + ' requested for transfer'}
            r = requests.post(utils.discordHookUrl, data=payload)

        c.connection.commit()
        c.connection.close()
        start_response("200 OK", [])
        return []

    def getHandled(self):
        return "requestTransfer"
