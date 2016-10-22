import json

import utils


def split(authors: str):
    return authors.split(",")


def handleAuthors(environ, start_response):
    c = utils.getCursor()
    c.execute("select distinct missionAuthor from missions order by missionAuthor")
    authors = c.fetchall()

    authorDto = [split(x['missionAuthor']) for x in authors]
    authorDto = [item for sublist in authorDto for item in sublist]
    authorDto = list(set(authorDto))
    encode = json.dumps(authorDto).encode()
    start_response("200 OK", [])
    return [encode]
