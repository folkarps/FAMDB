from urllib.parse import urlparse, parse_qs

import utils


def handleVersionDelete(request):
    c = utils.getCursor()

    o = parse_qs(urlparse(request.path).query)
    missionId = o['missionId']

    # if you're a low admin or this is your mission
    if utils.checkUserPermissions(utils.getCurrentUser(request), 2, missionId):
        request.wfile.write("Access Denied")
        return

    c.executemany('''update versions set toBeDeleted = 1 where missionId = ?''', {missionId})
    c.executemany('''delete from missions id = ''', {missionId})
    return
