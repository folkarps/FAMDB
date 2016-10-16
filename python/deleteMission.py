import json

import utils


def handleMissionDelete(request):
    c = utils.getCursor()

    missionJsonString = request.rfile.read1(99999999).decode()
    missionJson = json.loads(missionJsonString)
    missionId = missionJson['missionId']

    # if you're a low admin or this is your mission
    if not utils.checkUserPermissions(utils.getCurrentUser(request), 2, missionId):
        request.send_response(500)
        request.end_headers()
        request.wfile.write("Access Denied")
        return

    c.execute("delete from versions where missionId = ?", [missionId])
    c.execute("delete from missions where id = ?", [missionId])
    c.connection.commit()
    c.connection.close()
    request.send_response(200)
    request.end_headers()
    return
