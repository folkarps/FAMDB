import json

import utils


def handleArchive(request):
    c = utils.getCursor()
    missionJsonString = request.rfile.read1(99999999).decode()
    missionJson = json.loads(missionJsonString)
    missionId = missionJson['missionId']
    versionId = missionJson['versionId']
    origin = missionJson['origin']
    # if you're a low admin or this is your mission
    if not utils.checkUserPermissions(utils.getCurrentUser(request), 2, missionId):
        request.send_response(500)
        request.end_headers()
        request.wfile.write("Access Denied")
        return

    if origin == 'main':
        property = 'toBeArchivedMain'
    else:
        property = 'toBeArchivedMM'

    c.execute('''update versions set ''' + property + ''' = 1 where and id = ?''',
              [versionId])
    c.connection.commit()
    c.connection.close()
    return
