from urllib.parse import parse_qs

import utils


def handleDownload(environ, start_response):
    c = utils.getCursor()
    o = parse_qs(environ['QUERY_STRING'])
    versionId = o['versionId']
    c.execute("select * from versions where id = ?", versionId)
    version = c.fetchone()
    if version['existsOnMain'] == 1:
        dir = utils.missionMainDir
    else:
        dir = utils.missionMakerDir
    with open(dir + "/" + version['name'], mode="rb", ) as stream:
        start_response('200 OK', [('Content-Disposition', 'attachment; filename="' + version['name'] + '"')])
        return [stream.read()]
