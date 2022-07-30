import os

import utils
from handler import Handler


class CleanupHandler(Handler):
    def handle(self, environ, start_response):
        c = utils.getCursor()
        # if you're a low admin
        if not utils.checkUserPermissions(environ['user'], 2):
            start_response("403 Permission Denied", [])
            return ["Access Denied"]

        for origin in ['main', 'missionMaker']:
            if origin == 'main':
                missionDirPrefix = utils.missionMainDir
                toBeDeletedProperty = 'toBeDeletedMain'
                existsProperty = 'existsOnMain'
            else:
                missionDirPrefix = utils.missionMakerDir
                toBeDeletedProperty = 'toBeDeletedMM'
                existsProperty = 'existsOnMM'

            c.execute('''SELECT v.name, m.isCDLCMission FROM versions as v join missions as m on v.missionId = m.id WHERE v.''' + toBeDeletedProperty + ''' = 1''')
            toBeDeleted = c.fetchall()
            for (name, isCDLCMission) in toBeDeleted:
                # CDLC missions always live in missionMakerDir, so handle deletion of the actual file in a special case
                if isCDLCMission == 1:
                    continue

                try:
                    os.remove(os.path.join(missionDirPrefix, name))
                except OSError:
                    pass

            c.execute(
                "update versions set " + existsProperty + " = 0, " + toBeDeletedProperty + " = 0 where "
                + toBeDeletedProperty + " = 1")

        # Delete the CDLC PBO only if it's been "deleted" on both servers
        c.execute("SELECT v.name FROM versions as v join missions as m on v.missionId = m.id WHERE v.existsOnMM = 0 AND v.existsOnMain = 0 AND m.isCDLCMission = 1")
        cdlcToBeDeleted = c.fetchall()
        for row in cdlcToBeDeleted:
            try:
                os.remove(os.path.join(utils.missionMakerDir, row['name']))
            except OSError:
                pass

        # Clean-up versions with no files, and set missions with no versions (files) to the "Broken" status if not already Broken (or WIP)
        c.execute("DELETE FROM versions WHERE existsOnMM = 0 AND existsOnMain = 0")
        c.execute("SELECT id FROM missions WHERE status NOT IN ('WIP', 'Broken') AND id NOT IN (SELECT DISTINCT missionId from versions)")
        no_versions = c.fetchall()
        for row in no_versions:
            c.execute("UPDATE missions SET status ='Broken' WHERE id = ?", [row['id']])

        c.connection.commit()
        c.connection.close()

        start_response("200 OK", [])
        return []

    def getHandled(self):
        return "cleanup"
