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


def handleEditSession(request):
    c = utils.getCursor()
    editSessionString = request.rfile.read1(99999999).decode()
    editSessionJson = json.loads(editSessionString)

    if 'id' not in editSessionJson:
        c.execute("insert into sessions (date) values (?)", [editSessionJson['date']])
        c.execute("select max(id) from sessions")
        sessionId = c.fetchone()[0]
    else:
        sessionId = editSessionJson['id']

    c.execute("update sessions set missionNames = ?, host = ?, name = ?, players = ? where id = ? ",
              toParams(editSessionJson, sessionId))
    c.connection.commit()
    c.connection.close()
    request.send_header("location", sessionId)
    request.send_response(201)
    request.end_headers()
    return