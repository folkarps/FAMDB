from urllib.parse import parse_qs

import utils
from handler import Handler


class DownloadHandler(Handler):
    def handle(self, environ, start_response):
        c = utils.getCursor()
        o = parse_qs(environ['QUERY_STRING'])
        versionId = o['versionId']
        c.execute(
            "select v.existsOnMain, v.name, m.isCDLCMission from versions as v join missions as m on v.missionId = m.id where v.id = ?",
            versionId)
        (existsOnMain, name, isCDLCMission) = c.fetchone()
        # CDLC missions always live in missionMakerDir, so need to download from there instead
        if existsOnMain == 1 and isCDLCMission == 0:
            dir = utils.missionMainDir
        else:
            dir = utils.missionMakerDir
        with open(dir + "/" + name, mode="rb", ) as stream:
            start_response('200 OK', [('Content-Disposition', 'attachment; filename="' + name + '"')])
            return [stream.read()]

    def getHandled(self):
        return "download"
