import json

import utils


def toParams(editSessionJson, sessionId):
    params = []
    params.append(",".join(editSessionJson['missionNames']))
    params.append(editSessionJson['host'])
    params.append(editSessionJson['name'])
    params.append(editSessionJson['players'])
    params.append(sessionId)
    return params


def handleEditSession(environ, start_response):
    c = utils.getCursor()
    editSessionString = utils.environToContents(environ)
    editSessionJson = json.loads(editSessionString)
    sessionDate = editSessionJson['date']

    # if you're a low admin
    if not utils.checkUserPermissions(environ['user'], 2):
        start_response("403 Permission Denied", [])
        return ["Access Denied".encode()]

    if 'id' not in editSessionJson:
        c.execute("insert into sessions (date) values (?)", [sessionDate])
        c.execute("select max(id) from sessions")
        sessionId = c.fetchone()[0]
    else:
        sessionId = editSessionJson['id']

    c.execute("update sessions set missionNames = ?, host = ?, name = ?, players = ? where id = ? ",
              toParams(editSessionJson, sessionId))
    missions = editSessionJson['missionNames']
    for mission in missions:
        c.execute("update missions set playedCounter = playedCounter+1, lastPlayed=? where missionName =?",
                  [sessionDate, mission])
    c.connection.commit()
    c.connection.close()
    start_response("201 Created", [])
    return [("location:" + str(sessionId)).encode()]
