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

    if missionJson['needsRevision']:
        queryParts.append("needsRevision=?")
        params.append(1)

    queryParts.append("missionModified=?")
    params.append(date.today())
    return " , ".join(queryParts), params


def handleSaveMission(request):
    c = utils.getCursor()
    missionJsonString = request.rfile.read1(99999999).decode()
    missionJson = json.loads(missionJsonString)
    # create a blank row, then update that row so that we don't have 2 different statements
    if 'missionId' not in missionJson:
        c.execute("insert into missions (missionName) values (?)", [missionJson['missionName']])
        c.execute("select max(id) from missions")
        missionId = c.fetchone()[0]
    else:
        missionId = missionJson['missionId']
    query, params = constructQuery(missionJson)
    params.append(missionId)

    c.execute("update missions set " + query + "where id=?", params)
    c.connection.commit()
    c.connection.close()
    request.send_response(200)
    request.end_headers()
    return
