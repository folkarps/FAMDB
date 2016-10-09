import json

import utils


def handleVersionDelete(request):
    c = utils.getCursor()
    missionJsonString = request.rfile.read1(99999999).decode()
    missionJson = json.loads(missionJsonString)
    missionId = missionJson['missionId']
    versionId = missionJson['versionId']
    origin = missionJson['origin']
    # if you're a low admin or this is your mission
    if not utils.checkUserPermissions(utils.getCurrentUser(request), 2, missionId):
        request.wfile.write("Access Denied".encode())
        return

    if origin == 'main':
        property = 'toBeDeletedMain'
    else:
        property = 'toBeDeletedMM'

    c.execute('''update versions set ''' + property + ''' = 1 where id = ?''', [versionId])
    c.connection.commit()
    c.connection.close()
    request.send_response(200)
    request.end_headers()
    return
