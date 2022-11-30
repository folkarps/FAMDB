import json
import utils
from handler import Handler


class ValidTagsHandler(Handler):
    def handle(self, environ, start_response):
        c = utils.getCursor()
        c.execute('select tag from valid_tags')
        result = c.fetchall()
        valid_tags = [row['tag'] for row in result]
        encode = json.dumps(valid_tags).encode()
        start_response("200 OK", [])
        return [encode]

    def getHandled(self):
        return "validTags"
