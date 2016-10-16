import json
from urllib.parse import urlparse, parse_qs

import utils


def handleGetSession(request):
    c = utils.getCursor()
    o = parse_qs(urlparse(request.path).query)
    if "sessionId" in o:
        c.execute("select * from sessions where id = ?", [o['sessionId'][0]])
    else:
        c.execute("select * from sessions")
    sessions = c.fetchall()

    user = utils.getCurrentUser(request)
    sessionDtos = [dict(x) for x in sessions]
    for x in sessionDtos:
        x['missionNamesList'] = x['missionNames'].split(",")
        if user is not None:
            if user.permissionLevel >= 2:
                x['allowedToEdit'] = True

    request.wfile.write(json.dumps(sessionDtos).encode())
