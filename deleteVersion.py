import json

import utils


def handleVersionDelete(environ, start_response):
    c = utils.getCursor()
    missionJsonString = utils.environToContents(environ)
    missionJson = json.loads(missionJsonString)
    missionId = missionJson['missionId']
    versionId = missionJson['versionId']
    origin = missionJson['origin']
    # if you're a low admin or this is your mission
    if not utils.checkUserPermissions(environ['user'], 2, missionId):
        start_response("403 Permission Denied", [])
        return ["Access Denied"]

    if origin == 'main':
        property = 'toBeDeletedMain'
    else:
        property = 'toBeDeletedMM'

    c.execute('''update versions set ''' + property + ''' = 1 where id = ?''', [versionId])
    c.connection.commit()
    c.connection.close()

    start_response("200 OK", [])
    return []
