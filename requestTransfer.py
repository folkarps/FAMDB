import json
from pathlib import Path

import requests

import utils


def handleTransfer(environ, start_response):
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
        c.execute("update missions set status='Testing' where id = ?", [missionId])
        c.execute("update versions set requestedTransfer=1 where id = ?", [versionId])

    if utils.discordHookUrl != '':
        c.execute("select missionName, missionAuthor from missions where id = ?", [missionId])
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
