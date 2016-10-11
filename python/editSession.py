import json

import utils


def toParams(editSessionJson, sessionId):
    params = []
    params.append(",".join(editSessionJson['missionNames']))
    params.append(editSessionJson['host'])
    params.append(sessionId)
    return


def handleEditSession(request):
    c = utils.getCursor()
    editSessionString = request.rfile.read1(99999999).decode()
    editSessionJson = json.loads(editSessionString)

    if 'id' not in editSessionJson:
        c.execute("insert into sessions (date) values (?)", editSessionJson['date'])
        c.execute("select max(id) from sessions")
        sessionId = c.fetchone()
    else:
        sessionId = editSessionJson['id']

    c.execute("update sessions set missionNames = ?, host = ? where id = ? ", toParams(editSessionJson, sessionId))
