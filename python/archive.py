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

    if o['origin'][0] == 'main':
        property = 'toBeArchivedMain'
    else:
        property = 'toBeArchivedMM'

    c.executemany('''update versions set ''' + property + ''' = 1 where and name = ?''',
                  [o['name'][0]])
    return
