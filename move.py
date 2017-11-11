import json
from pathlib import Path
from shutil import copyfile

import requests

import utils


def authorToUser(author):
    c = utils.getCursor()
    c.execute("select discordId from users where login = ?", [author])
    return c.fetchone()[0]


def handleMove(environ, start_response):
    user = environ['user']
    missionJsonString = utils.environToContents(environ)
    missionJson = json.loads(missionJsonString)
    missionId = missionJson['missionId']
    versionId = missionJson['versionId']
    # If you're a MM user and this is your mission, or you're a low admin
    if not (utils.checkUserPermissions(user, 1, missionId=missionId, collector=utils.AND) or utils.checkUserPermissions(
            user, 2)):
        start_response("403 Permission Denied", [])
        return ["Access Denied"]

    c = utils.getCursor()
    c.execute("select name from versions where id = ?", [versionId])

    fileName = c.fetchone()[0]
    if Path(utils.missionMakerDir + "/" + fileName).exists():
        copyfile(utils.missionMakerDir + "/" + fileName, utils.missionMainDir + "/" + fileName)
        c.execute("UPDATE versions SET existsOnMain=1, requestedTransfer=0, requestedTesting=0 WHERE id = ?",
                  [versionId])

        c.execute("update missions set status ='Ready' where id = ?", [missionId])

    if utils.discordHookUrl != '':
        c.execute("select missionAuthor from missions where id = ?", [missionId])
        missionFromDb = c.fetchone()
        missionAuthorDiscordIds = filter(None, [authorToUser(author) for author in missionFromDb[0].split(",")])
        missionAuthorDiscordIds = ['<@' + discordId + ">" for discordId in missionAuthorDiscordIds]

        payload = {'content': 'Rejoice  ' + ' '.join(missionAuthorDiscordIds) + '! ' + fileName + ' has been accepted'}

        r = requests.post(utils.discordHookUrl, data=payload)

    c.connection.commit()
    c.connection.close()
    start_response("200 OK", [])
    return []
