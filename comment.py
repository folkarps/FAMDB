import html
import json
from datetime import datetime

import requests

import utils


def authorToUser(author):
    c = utils.getCursor()
    c.execute("select discordId from users where login = ?", [author])
    user = c.fetchone()
    return None if user is None else user[0]


def handleComment(environ, start_response):
    user = environ['user']
    missionJsonString = utils.environToContents(environ)
    missionJson = json.loads(missionJsonString)
    missionId = missionJson['missionId']
    comment = html.escape(missionJson['comment'])
    rejection = True if 'rejection' in missionJson and missionJson['rejection'] == 'true' else False
    # If you're a MM user and this is your mission, or you're a low admin
    if rejection and not (
                utils.checkUserPermissions(user, 1, missionId=missionId,
                                           collector=utils.AND) or utils.checkUserPermissions(
            user, 2)):
        start_response("403 Permission Denied", [])
        return ["Access Denied"]

    c = utils.getCursor()
    c.execute("select name, id from versions where id = (select max(id) from versions where missionId = ?)",
              [missionId])

    versionRow = c.fetchone()
    fileName = versionRow[0]
    versionId = versionRow[1]

    c.execute("update missions set status ='WIP' where id = ?", [missionId])
    c.execute("insert into comments (missionId, user, contents, createDate, versionId) values (?,?,?,?, ?)",
              [missionId, user.login, comment, datetime.now(), versionId])

    if utils.discordHookUrl != '':
        c.execute("select missionName, missionAuthor from missions where id = ?", [missionId])
        missionFromDb = c.fetchone()
        missionName = missionFromDb[0]
        missionAuthorDiscordIds = filter(None, [authorToUser(author) for author in missionFromDb[1].split(",")])
        missionAuthorDiscordIds = ['<@' + discordId + ">" for discordId in missionAuthorDiscordIds]

        if rejection:
            payload = {
                'content': 'Despair  ' + ' '.join(missionAuthorDiscordIds) + '! ' + fileName + ' has been rejected'}
        else:
            payload = {'content': ' '.join(missionAuthorDiscordIds) + '! ' + missionName + ' has a new comment. '}
        r = requests.post(utils.discordHookUrl, data=payload)

    c.connection.commit()
    c.connection.close()
    start_response("200 OK", [])
    return []
