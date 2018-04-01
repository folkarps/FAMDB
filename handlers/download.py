from urllib.parse import parse_qs

import utils
from handler import Handler


class DownloadHandler(Handler):
    def handle(self, environ, start_response):
        c = utils.getCursor()
        o = parse_qs(environ['QUERY_STRING'])
        versionId = o['versionId']
        c.execute("SELECT * FROM versions WHERE id = ?", versionId)
        version = c.fetchone()
        if version['existsOnMain'] == 1:
            dir = utils.missionMainDir
        else:
            dir = utils.missionMakerDir
        with open(dir + "/" + version['name'], mode="rb", ) as stream:
            start_response('200 OK', [('Content-Disposition', 'attachment; filename="' + version['name'] + '"')])
            return [stream.read()]

    def getHandled(self):
        return "download"
