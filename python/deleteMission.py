from urllib.parse import urlparse, parse_qs

import utils


def handleVersionDelete(request):
    c = utils.getCursor()

    o = parse_qs(urlparse(request.path).query)
    c.executemany('''update versions set toBeDeleted = 1 where missionId = ?''', {o['missionId']})
    c.executemany('''delete from missions id = ''', {o['missionId']})
    return
