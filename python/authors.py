import json

import utils


def split(authors: str):
    return authors.split(",")


def handleAuthors(request):
    c = utils.getCursor()
    c.execute("select distinct missionAuthor from missions order by missionAuthor")
    authors = c.fetchall()

    authorDto = [split(x['missionAuthor']) for x in authors]
    authorDto = [item for sublist in authorDto for item in sublist]
    encode = json.dumps(authorDto).encode()
    request.wfile.write(encode)
    return
