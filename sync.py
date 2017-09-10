import itertools
from pathlib import Path

import utils


def handleSync(environ, start_response):
    c = utils.getCursor()
    if utils.checkUserPermissions(environ['user'], 3):

        c.execute(str.format('''select * from versions order by missionId'''))
        versionsFromDb = c.fetchall()

        for version in versionsFromDb:
            existsOnMM = False
            if version['existsOnMM']:
                existsOnMM = True
                if not Path(utils.missionMakerDir + "/" + version['name']).is_file():
                    existsOnMM = False
                    c.execute(str.format('''update versions set existsOnMM=0 where id = {}''', version['id']))

            existsOnMain = False
            if version['existsOnMain']:
                existsOnMain = True
                if not Path(utils.missionMainDir + "/" + version['name']).is_file():
                    existsOnMain = False
                    c.execute(str.format('''update versions set existsOnMain=0 where id = {}''', version['id']))

            if not existsOnMain and not existsOnMM:
                c.execute(str.format('''delete from versions where id = {}''', version['id']))

        # group the mission by their mission Id
        versionsGroupedByMission = {}
        for k, g in itertools.groupby(versionsFromDb, lambda x: x['missionId']):
            versionsGroupedByMission[k] = list(g)

        c.connection.commit()
        c.connection.close()
    else:
        start_response("403 Permission Denied", [])
        return ["Access Denied".encode()]

    start_response("200 OK", [])
    return []
