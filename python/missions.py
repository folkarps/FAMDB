import itertools
import json
import sqlite3
from urllib.parse import urlparse, parse_qs


def handleMissions(request):
    conn = sqlite3.connect('famdb.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    o = parse_qs(urlparse(request.path).query)
    query, params = constructQuery(o)
    # retrieve all the missions that match our parameters
    c.execute('''select * from missions where ''' + query, params)
    missionsFromDb = c.fetchall()

    # if any missions were returned, return all versions associated with those missions
    if (len(missionsFromDb) > 0):
        ids = [str(x['id']) for x in missionsFromDb]
        # sqlite can't take lists, so we need to transform it into a string
        #    then format the string into the query so that it doesn't get treated as a string
        idParameter = ",".join(ids)

        c.execute(str.format('''select * from versions where missionId in ({}) order by missionId''', idParameter))
        versionsFromDb = c.fetchall()
        # group the mission by their mission Id
        versionsGroupedByMission = list(itertools.groupby(versionsFromDb, lambda x: x['missionId']))
    else:
        versionsGroupedByMission = []

    # groupby has returned these as a list of tuple(missionId, list(version))
    #  we want a map so that we can do key access
    versionMap = dict(versionsGroupedByMission)

    # transform the row objects into objects that can be serialized
    m = [toDto(x, versionMap) for x in missionsFromDb]
    encode = json.dumps(m).encode()
    request.wfile.write(encode)
    return


# copy the variables out of the non-serializable db object into a blank object
def toDto(missionFromDb, verionsGrouped):
    dto = toDtoHelper(missionFromDb)
    if (dto['id'] in verionsGrouped):
        dto['versions'] = [toDtoHelper(version) for version in verionsGrouped[dto['id']]]
    return dto


def toDtoHelper(version):
    return dict(version)


def constructQuery(params):
    query = []
    p = []
    if ("map" in params) & (params['map'][0] != 'All Maps'):
        query.append('missionMap = ?')
        p.append(params['map'][0])
    if ("author" in params) & (params['author'][0] != 'All Authors'):
        query.append("missionAuthor = ?")
        p.append(params['author'][0])
    if "isBroken" in params:
        query.append("isBroken = ?")
        p.append(params['isBroken'][0])
    if "needsRevision" in params:
        query.append("needsRevision = ?")
        p.append(params['needsRevision'][0])
    if "missionTypes[]" in params:
        missionTypeString = ["'{0}'".format(w) for w in params['missionTypes[]']]
        query.append(str.format("missionType in({})", ",".join(missionTypeString)))
    if "name" in params:
        query.append("missionName  = ?")
        p.append(params['name'][0])
    if "playerMax" in params:
        query.append("missionPlayers  <= ? ")
        p.append(params['playerMax'][0])
    if "playerMin" in params:
        query.append("missionPlayers  >= ? ")
        p.append(params['playerMin'][0])
    return " AND ".join(query), p
