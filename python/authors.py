import json

import utils


def handleAuthors(request):
    c = utils.getCursor()
    c.execute("select distinct missionAuthor from missions order by missionAuthor")
    authors = c.fetchall()
    authorDto = [x['missionAuthor'] for x in authors]
    encode = json.dumps(authorDto).encode()
    request.wfile.write(encode)
    return
