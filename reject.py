import json

import requests

import utils


def authorToUser(author):
    c = utils.getCursor()
    c.execute("select discordId from users where login = ?", [author])
    return c.fetchone()[0]


def handleReject(environ, start_response):
    user = environ['user']
    missionJsonString = utils.environToContents(environ)
    missionJson = json.loads(missionJsonString)
    missionId = missionJson['missionId']
    versionId = missionJson['versionId']
    comment = missionJson['comment']
    # If you're a MM user and this is your mission, or you're a low admin
    if not (utils.checkUserPermissions(user, 1, missionId=missionId, collector=utils.AND) or utils.checkUserPermissions(
            user, 2)):
        start_response("403 Permission Denied", [])
        return ["Access Denied"]

    c = utils.getCursor()
    c.execute("select name from versions where id = ?", [versionId])

    fileName = c.fetchone()[0]

    c.execute("update missions set status ='WIP' where id = ?", [missionId])
    c.execute("insert into comments (versionId, userId, comment) values (?,?,?)", versionId, user.id, comment)

    if utils.discordHookUrl != '':
        c.execute("select missionAuthor from missions where id = ?", [missionId])
        missionFromDb = c.fetchone()
        missionAuthorDiscordIds = filter(None, [authorToUser(author) for author in missionFromDb[0].split(",")])
        missionAuthorDiscordIds = ['<@' + discordId + ">" for discordId in missionAuthorDiscordIds]

        payload = {'content': 'Despair  ' + ' '.join(missionAuthorDiscordIds) + '! ' + fileName + ' has been rejected'}

        r = requests.post(utils.discordHookUrl, data=payload)

    start_response("200 OK", [])
    return []
