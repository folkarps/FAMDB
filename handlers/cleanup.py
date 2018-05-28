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

            c.execute('''SELECT * FROM versions WHERE ''' + toBeDeletedProperty + ''' = 1''')
            toBeDeleted = c.fetchall()
            for deleteMe in toBeDeleted:
                try:
                    os.remove(os.path.join(missionDirPrefix, deleteMe['name']))
                except OSError:
                    pass

            c.execute(
                "update versions set " + existsProperty + " = 0, " + toBeDeletedProperty + " = 0 where "
                + toBeDeletedProperty + " = 1")
        c.execute("SELECT id FROM versions WHERE existsOnMM = 0 AND existsOnMain = 0")

        c.execute("DELETE FROM versions WHERE existsOnMM = 0 AND existsOnMain = 0")
        c.connection.commit()
        c.connection.close()

        start_response("200 OK", [])
        return []

    def getHandled(self):
        return "cleanup"
