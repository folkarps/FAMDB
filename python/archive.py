from urllib.parse import urlparse, parse_qs

import utils


def handleArchive(request):
    c = utils.getCursor()
    o = parse_qs(urlparse(request.path).query)

    missionId = o['missionId'][0]
    # if you're a low admin or this is your mission
    if not utils.checkUserPermissions(utils.getCurrentUser(request), 2, missionId):
        request.wfile.write("Access Denied")
        return

    c.executemany('''update versions set toBeArchived = 1 where origin = ? and name = ?''',
                  {o['origin'][0], o['name'][0]})
    return
