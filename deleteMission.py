import json

import utils


def handleMissionDelete(environ, start_response):
    c = utils.getCursor()

    missionJsonString = utils.environToContents(environ)
    missionJson = json.loads(missionJsonString)
    missionId = missionJson['missionId']

    # if you're a low admin or this is your mission
    if not utils.checkUserPermissions(environ['user'], 2, missionId):
        start_response("403 Permission Denied", [])
        return ["Access Denied"]

    c.execute("delete from versions where missionId = ?", [missionId])
    c.execute("delete from missions where id = ?", [missionId])
    c.connection.commit()
    c.connection.close()
    start_response("200 OK", [])
    return []
