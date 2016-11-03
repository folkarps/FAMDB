import json
from datetime import date

import utils


def constructQuery(missionJson):
    queryParts = []
    params = []

    for part in ['missionAuthor', 'missionPlayers', 'missionMap', 'missionType', 'missionDesc', 'missionNotes',
                 'framework']:
        queryParts.append(part + "=?")
        params.append(missionJson[part])

    if missionJson['isBroken']:
        queryParts.append("isBroken=?")
        params.append(1)
    else:
        queryParts.append("isBroken=?")
        params.append(0)


    if missionJson['needsRevision']:
        queryParts.append("needsRevision=?")
        params.append(1)
    else:
        queryParts.append("needsRevision=?")
        params.append(0)

    queryParts.append("missionModified=?")
    params.append(date.today())
    return " , ".join(queryParts), params


def handleSaveMission(environ, start_response):
    c = utils.getCursor()
    missionJsonString = utils.environToContents(environ)
    missionJson = json.loads(missionJsonString)
    # create a blank row, then update that row so that we don't have 2 different statements
    if 'missionId' not in missionJson:
        c.execute("insert into missions (missionName) values (?)", [missionJson['missionName']])
        c.execute("select max(id) from missions")
        missionId = c.fetchone()[0]
        hasPermissions = utils.checkUserPermissions(environ['user'], 0)
    else:
        missionId = missionJson['missionId']
        c.execute("select * from missions where id = ?", [missionId])
        mission = c.fetchone()
        if mission is None:
            start_response("500 Internal Server Response", [])
            return ["Stop trying to edit a mission that doesn't exist".encode()]
        hasPermissions = utils.checkUserPermissions(environ['user'], 2, missionId)

    if not hasPermissions:
        start_response("403 Permission Denied", [])
        return ["Access Denied"]
    query, params = constructQuery(missionJson)
    params.append(missionId)

    c.execute("update missions set " + query + "where id=?", params)
    c.connection.commit()
    c.connection.close()
    start_response("201 Created", [])
    return [(str(missionId)).encode()]
