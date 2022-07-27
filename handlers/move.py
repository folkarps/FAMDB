import json
from pathlib import Path
from shutil import copyfile

import requests

import utils
from handler import Handler


class MoveHandler(Handler):
    def handle(self, environ, start_response):
        user = environ['user']
        missionJsonString = utils.environToContents(environ)
        missionJson = json.loads(missionJsonString)
        missionId = missionJson['missionId']
        versionId = missionJson['versionId']
        # If you're a MM user and this is your mission, or you're a low admin
        if not (
                    utils.checkUserPermissions(user, 1, missionId=missionId,
                                               collector=utils.AND) or utils.checkUserPermissions(
                    user, 2)):
            start_response("403 Permission Denied", [])
            return ["Access Denied"]

        c = utils.getCursor()
        c.execute("select versions.name, missions.isCDLCMission from versions join missions on versions.missionId = missions.id where versions.id = ?", [versionId])
        (fileName, isCDLCMission) = c.fetchone()

        if Path(utils.missionMakerDir + "/" + fileName).exists():
            # CDLC missions always live in missionMakerDir, so don't actually move the file, just pretend to
            if isCDLCMission == 0:
                copyfile(utils.missionMakerDir + "/" + fileName, utils.missionMainDir + "/" + fileName)
            c.execute("UPDATE versions SET existsOnMain=1, requestedTransfer=0, requestedTesting=0 WHERE id = ?",
                      [versionId])

            c.execute("UPDATE missions SET status ='Ready' WHERE id = ?", [missionId])

        if utils.discordHookUrl != '':
            c.execute("SELECT missionAuthor FROM missions WHERE id = ?", [missionId])
            missionFromDb = c.fetchone()
            missionAuthorDiscordIds = filter(None, [authorToUser(author) for author in missionFromDb[0].split(",")])
            missionAuthorDiscordIds = ['<@' + discordId + ">" for discordId in missionAuthorDiscordIds]

            if missionAuthorDiscordIds:
                payload = {
                    'content': 'Rejoice  ' + ' '.join(missionAuthorDiscordIds) + '! ' + fileName + ' has been accepted'}
            else:
                payload = {
                    'content': 'Rejoice  ' + missionFromDb[0] + ':RIP:! ' + fileName + ' has been accepted'}

            r = requests.post(utils.discordHookUrl, data=payload)

        c.connection.commit()
        c.connection.close()
        start_response("200 OK", [])
        return []

    def getHandled(self):
        return "move"


def authorToUser(author):
    c = utils.getCursor()
    c.execute("SELECT discordId FROM users WHERE login = ?", [author.strip()])
    fetchone = c.fetchone()
    if fetchone:
        return fetchone[0]
    else:
        return None
