from urllib.parse import urlparse, parse_qs

import utils


def handleArchive(request):
    c = utils.getCursor()
    o = parse_qs(urlparse(request.path).query)
    c.executemany('''update versions set toBeArchived = 1 where origin = ? and name = ?''', {o['origin'], o['name']})
    return
