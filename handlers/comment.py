import html
import json
from datetime import datetime

import requests

import utils
from handler import Handler


class CommentHandler(Handler):
    def handle(self, environ, start_response):
        user = environ['user']
        missionJsonString = utils.environToContents(environ)
        missionJson = json.loads(missionJsonString)
        missionId = missionJson['missionId']
        comment = html.escape(missionJson['comment'])
        rejection = True if 'rejection' in missionJson and missionJson['rejection'] == True else False
        # If you're a MM user and this is your mission, or you're a low admin
        if rejection and not (
                    utils.checkUserPermissions(user, 1, missionId=missionId,
                                               collector=utils.AND) or utils.checkUserPermissions(
                    user, 2)):
            start_response("403 Permission Denied", [])
            return ["Access Denied"]

        c = utils.getCursor()
        c.execute("SELECT name, id FROM versions WHERE id = (SELECT max(id) FROM versions WHERE missionId = ?)",
                  [missionId])

        versionRow = c.fetchone()
        fileName = versionRow[0]
        versionId = versionRow[1]

        if rejection:
            c.execute("UPDATE missions SET status ='Broken' WHERE id = ?", [missionId])
            c.execute("UPDATE versions SET requestedTransfer=0, requestedTesting=0 WHERE id = ?", [versionId])
        c.execute("INSERT INTO comments (missionId, user, contents, createDate, versionId) VALUES (?,?,?,?, ?)",
                  [missionId, user.login, comment, datetime.now(), versionId])

        if utils.discordHookUrl != '':
            c.execute("SELECT missionName, missionAuthor FROM missions WHERE id = ?", [missionId])
            missionFromDb = c.fetchone()
            missionName = missionFromDb[0]
            unawareAuthors = filter(lambda author: author.strip() != user.login,
                                    [author for author in missionFromDb[1].split(",")])
            missionAuthorDiscordIds = filter(None, [authorToUser(author) for author in unawareAuthors])

            # Only send the message if there is at least one ID to send to
            if len(list(missionAuthorDiscordIds)) > 0:
                missionAuthorDiscordIds = ['<@' + discordId + ">" for discordId in missionAuthorDiscordIds]

                if rejection:
                    payload = {
                        'content': 'Despair  ' + ' '.join(
                            missionAuthorDiscordIds) + '! ' + fileName + ' has been rejected'}
                else:
                    payload = {
                        'content': ' '.join(missionAuthorDiscordIds) + '! ' + missionName + ' has a new comment. '}
                r = requests.post(utils.discordHookUrl, data=payload)

        c.connection.commit()
        c.connection.close()
        start_response("200 OK", [])
        return []

    def getHandled(self):
        return "comment"


def authorToUser(author):
    c = utils.getCursor()
    c.execute("SELECT discordId FROM users WHERE login = ?", [author])
    user = c.fetchone()
    return None if user is None else user[0]
