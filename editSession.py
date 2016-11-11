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

    c.execute("select missionNames from sessions where id = ?", [sessionId])
    existingMissionNames = c.fetchone()

    c.execute("update sessions set missionNames = ?, host = ?, name = ?, players = ? where id = ? ",
              toParams(editSessionJson, sessionId))
    missions = editSessionJson['missionNames']

    newMissions = []

    if existingMissionNames['missionNames'] is not None:
        existingMissionNames = existingMissionNames['missionNames'].split(",")
        for mission in missions:
            if mission in existingMissionNames:
                existingMissionNames.remove(mission)
            else:
                newMissions.append(mission)
    else:
        newMissions = missions

    for mission in newMissions:
        c.execute("update missions set playedCounter = playedCounter+1, lastPlayed=? where missionName =?",
                  [sessionDate, mission])
    c.connection.commit()
    c.connection.close()
    start_response("201 Created", [])
    return [("location:" + str(sessionId)).encode()]
