from urllib.parse import urlparse, parse_qs

import utils


def handleSetUserLevel(request):
    c = utils.getCursor()
    o = parse_qs(urlparse(request.path).query)
    userId = o['id']
    level = o['level']
    c.execute("update users set permissionLevel = ? where id = ?", [level, userId])
    return
