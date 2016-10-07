from urllib.parse import urlparse, parse_qs

import utils


def handleVersionDelete(request):
    c = utils.getCursor()
    o = parse_qs(urlparse(request.path).query)
    c.executemany('''update versions set toBeDeleted = 1 where origin = ? and name = ?''', {o['origin'], o['name']})
    return
