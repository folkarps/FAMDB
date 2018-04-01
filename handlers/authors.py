import json

import utils
from handler import Handler


class AuthorHandler(Handler):
    def handle(self, environ, start_response):
        c = utils.getCursor()
        c.execute("SELECT DISTINCT missionAuthor FROM missions ORDER BY missionAuthor")
        authors = c.fetchall()

        authorDto = [AuthorHandler.__split(self, x['missionAuthor']) for x in authors]
        authorDto = [item.strip() for sublist in authorDto for item in sublist]
        authorDto = list(sorted(set(authorDto), key=lambda s: s.lower()))
        encode = json.dumps(authorDto).encode()
        start_response("200 OK", [])
        return [encode]

    def getHandled(self):
        return "authors"

    def __split(self, authors: str):
        return authors.split(",")
