import os
from http import cookies
from http.cookies import SimpleCookie

import utils
from handler import Handler
import handlers

subclasses = Handler.__subclasses__()
handlerInstances = {subclass().getHandled(): subclass().handle for (subclass) in subclasses}


def wsgi(environ, start_response):
    path = environ['PATH_INFO']
    simplePath = path.replace("/", "")
    if "HTTP_COOKIE" in environ:
        cookie = SimpleCookie(environ['HTTP_COOKIE'])
        environ['user'] = utils.getCurrentUser(cookie)
    else:
        environ['HTTP_COOKIE'] = None
        environ['user'] = None
    if simplePath in handlerInstances:
        return handlerInstances[simplePath](environ, start_response)
    else:
        responseHeaders = utils.handleBadSessionIds(environ)

        permissionCookie = SimpleCookie(environ['HTTP_COOKIE'])
        if 'permissionLevel' in permissionCookie:
            cookiePermissionLevel = permissionCookie['permissionLevel'].value
            if environ['user'] is not None and str(environ['user'].permissionLevel) != cookiePermissionLevel:
                cookie = cookies.SimpleCookie()
                cookie['permissionLevel'] = environ['user'].permissionLevel
                responseHeaders.append(('set-cookie', cookie.output(header='')))
        if path == '/':
            path = '/index.html'
        filePath = utils.currentPath + '/static' + path
        with open(filePath, mode="rb", ) as stream:
            statbuf = os.stat(filePath)
            if 'HTTP_IF_NONE_MATCH' in environ:
                if environ['HTTP_IF_NONE_MATCH'] == str(statbuf.st_mtime):
                    start_response('304 NOT MODIFIED', responseHeaders)
                    return [''.encode()]
            responseHeaders.append(('ETag', str(statbuf.st_mtime)))
            start_response('200 OK', responseHeaders)
            return [stream.read()]
