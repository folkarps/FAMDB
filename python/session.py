import json

import utils


def handleGetSession(request):
    c = utils.getCursor()
    c.execute("select * from sessions")
    sessions = c.fetchall()

    sessionDtos = [dict(x) for x in sessions]
    for x in sessionDtos:
        x['missionNamesList'] = x['missionNames'].split(",")

    request.wfile.write(json.dumps(sessionDtos).encode())
