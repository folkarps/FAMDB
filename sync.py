import itertools
import os
import re
from datetime import date
from pathlib import Path

import utils


def sanatizeFileName(x: str):
    x = x.replace('fa3_', '')
    x = re.sub(r'(a|c)\d+', "", x)
    x = re.sub(r'v(t)?\d+.*', "", x)
    x = x.replace("_", "")
    return x


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

        c.connection.commit()
        c.connection.close()

        c = utils.getCursor()

        c.execute('''select id, missionName from missions''')

        missions = c.fetchall()
        fileNames = os.listdir(utils.missionMakerDir)

        filesGroupedByMissionName = {}
        for k, g in itertools.groupby(fileNames, lambda x: sanatizeFileName(x)):
            filesGroupedByMissionName[k] = list(g)

        c.execute('''select name from versions''')
        versionRows = c.fetchall()
        versions = [x['name'] for x in versionRows]

        # for each db mission
        # find all files that match
        # for each file
        # find out if file is in db
        # if not
        # add to db
        for mission in missions:
            sanitizedName = mission['missionName'].lower().replace(' ', '')
            if sanitizedName in filesGroupedByMissionName:

                filesForThisMission = filesGroupedByMissionName[sanitizedName]
                for fileForThisMission in filesForThisMission:
                    if not fileForThisMission in versions:
                        c.execute(
                            "insert into versions(missionId, name, createDate) values (?, ?, ?)",
                            [mission['id'], fileForThisMission, date.today()])

                    c.execute("update versions set existsOnMM = 1 where name = ?", [fileForThisMission])

        c.connection.commit()
        c.connection.close()

        c = utils.getCursor()

        fileNames = os.listdir(utils.missionMainDir)

        filesGroupedByMissionName = {}
        for k, g in itertools.groupby(fileNames, lambda x: sanatizeFileName(x)):
            filesGroupedByMissionName[k] = list(g)

        c.execute('''select name from versions''')
        versionRows = c.fetchall()
        versions = [x['name'] for x in versionRows]

        # for each db mission
        # find all files that match
        # for each file
        # find out if file is in db
        # if not
        # add to db
        for mission in missions:
            sanitizedName = mission['missionName'].lower().replace(' ', '')
            if sanitizedName in filesGroupedByMissionName:

                filesForThisMission = filesGroupedByMissionName[sanitizedName]
                for fileForThisMission in filesForThisMission:
                    if not fileForThisMission in versions:
                        c.execute(
                            "insert into versions(missionId, name, createDate, existsOnMM) values (?, ?, ?, ?)",
                            [mission['id'], fileForThisMission, date.today(), False])
                    c.execute("update versions set existsOnMain = 1 where name = ?", [fileForThisMission])

        c.connection.commit()
        c.connection.close()


    else:
        start_response("403 Permission Denied", [])
        return ["Access Denied".encode()]

    start_response("200 OK", [])
    return []
