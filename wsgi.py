from http import cookies
from http.cookies import SimpleCookie

import utils
from archive import handleArchive
from authors import handleAuthors
from changePasswordInternal import handleChangePassword
from cleanup import handleCleanup
from createUser import handleCreateUser
from deleteMission import handleMissionDelete
from deleteSession import handleSessionDelete
from deleteVersion import handleVersionDelete
from download import handleDownload
from editSession import handleEditSession
from login import handleLogin
from missions import handleMissions
from move import handleMove
from resetPassword import handleResetPassword
from saveMission import handleSaveMission
from session import handleGetSession
from setPermissionLevel import handlePermissionLevel
from sync import handleSync
from upload import handleUpload
from users import handleUsers

handlers = {'deleteVersion': handleVersionDelete, 'login': handleLogin, 'signup': handleCreateUser,
            'move': handleMove, 'archive': handleArchive, 'cleanup': handleCleanup, 'upload': handleUpload,
            'saveMission': handleSaveMission, "setPermissionLevel": handlePermissionLevel,
            "editSession": handleEditSession, "deleteSession": handleSessionDelete,
            "deleteMission": handleMissionDelete, 'missions': handleMissions, 'authors': handleAuthors,
            'users': handleUsers, 'sessions': handleGetSession, 'download': handleDownload,
            'resetPassword': handleResetPassword, 'changePasswordInternal': handleChangePassword, 'sync': handleSync}


def wsgi(environ, start_response):
    path = environ['PATH_INFO']
    simplePath = path.replace("/", "")
    if "HTTP_COOKIE" in environ:
        cookie = SimpleCookie(environ['HTTP_COOKIE'])
        environ['user'] = utils.getCurrentUser(cookie)
    else:
        environ['HTTP_COOKIE'] = None
        environ['user'] = None
    if simplePath in handlers:
        return handlers[simplePath](environ, start_response)
    else:
        responseHeaders = utils.handleBadSessionIds(environ)

        permissionCookie = SimpleCookie(environ['HTTP_COOKIE'])
        if 'permissionLevel' in permissionCookie:
            cookiePermissionLevel = permissionCookie['permissionLevel'].value
            if environ['user'] is not None and str(environ['user'].permissionLevel) != cookiePermissionLevel:
                cookie = cookies.SimpleCookie()
                cookie['permissionLevel'] = environ['user'].permissionLevel
                responseHeaders.append(('set-cookie', cookie.output(header='')))

        responseHeaders.append(('Cache-Control', 'max-age=86400'))
        if path == '/':
            path = '/index.html'
        with open(utils.currentPath + '/static' + path, mode="rb", ) as stream:
            start_response('200 OK', responseHeaders)
            return [stream.read()]
