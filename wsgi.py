from http.cookies import SimpleCookie

import utils
from archive import handleArchive
from authors import handleAuthors
from cleanup import handleCleanup
from createUser import handleCreateUser
from deleteMission import handleMissionDelete
from deleteSession import handleSessionDelete
from deleteVersion import handleVersionDelete
from editSession import handleEditSession
from login import handleLogin
from missions import handleMissions
from move import handleMove
from saveMission import handleSaveMission
from session import handleGetSession
from setPermissionLevel import handlePermissionLevel
from upload import handleUpload
from users import handleUsers

handlers = {'deleteVersion': handleVersionDelete, 'login': handleLogin, 'signup': handleCreateUser,
            'move': handleMove, 'archive': handleArchive, 'cleanup': handleCleanup, 'upload': handleUpload,
            'saveMission': handleSaveMission, "setPermissionLevel": handlePermissionLevel,
            "editSession": handleEditSession, "deleteSession": handleSessionDelete,
            "deleteMission": handleMissionDelete, 'missions': handleMissions, 'authors': handleAuthors,
            'users': handleUsers, 'sessions': handleGetSession}

from handleDbStart import initDb

initDb()


def handleWSGI(environ, start_response):
    path = environ['PATH_INFO']
    simplePath = path.replace("/", "")
    cookie = SimpleCookie(environ['HTTP_COOKIE'])
    environ['user'] = utils.getCurrentUser(cookie)
    if simplePath in handlers:
        return handlers[simplePath](environ, start_response)
    else:
        responseHeaders = utils.handleBadSessionIds(environ)
        with open('static' + path, mode="rb", ) as stream:
            start_response('200 OK', responseHeaders)
            return [stream.read()]
