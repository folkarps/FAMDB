import itertools
import os
import re
from datetime import date
from pathlib import Path

import utils
from handler import Handler


class SyncHandler(Handler):
    def handle(self, environ, start_response):
        c = utils.getCursor()
        if utils.checkUserPermissions(environ['user'], 3):

            c.execute(str.format('''SELECT v.id, v.name, v.existsOnMM, v.existsOnMain, m.isCDLCMission FROM versions as v join missions as m on v.missionId = m.id ORDER BY v.missionId'''))
            versionsFromDb = c.fetchall()

            for version in versionsFromDb:
                existsOnMM = False
                if version['existsOnMM']:
                    existsOnMM = True
                    if not Path(utils.missionMakerDir + "/" + version['name']).is_file():
                        existsOnMM = False
                        c.execute(str.format('''UPDATE versions SET existsOnMM=0 WHERE id = {}''', version['id']))

                existsOnMain = False
                if version['existsOnMain']:
                    existsOnMain = True
                    # CDLC missions only live in the MM directory, even if existsOnMain is true, so don't try it
                    if version['isCDLCMission'] == 0 and not Path(utils.missionMainDir + "/" + version['name']).is_file():
                        existsOnMain = False
                        c.execute(str.format('''UPDATE versions SET existsOnMain=0 WHERE id = {}''', version['id']))

                if not existsOnMain and not existsOnMM:
                    c.execute(str.format('''DELETE FROM versions WHERE id = {}''', version['id']))

            c.connection.commit()
            c.connection.close()

            c = utils.getCursor()

            c.execute('''SELECT id, missionName FROM missions''')

            missions = c.fetchall()
            fileNames = os.listdir(utils.missionMakerDir)

            filesGroupedByMissionName = {}
            for k, g in itertools.groupby(fileNames, lambda x: SyncHandler.sanatizeFileName(self, x)):
                filesGroupedByMissionName[k] = list(g)

            c.execute('''SELECT name FROM versions''')
            versionRows = c.fetchall()
            versions = [x['name'] for x in versionRows]

            # for each db mission
            # find all files that match
            # for each file
            # find out if file is in db
            # if not
            # add to db
            for mission in missions:
                sanitizedName = SyncHandler.sanatizeMissionName(self, mission['missionName'])
                if sanitizedName in filesGroupedByMissionName:

                    filesForThisMission = filesGroupedByMissionName[sanitizedName]
                    for fileForThisMission in filesForThisMission:
                        if not fileForThisMission in versions:
                            c.execute(
                                "INSERT INTO versions(missionId, name, createDate) VALUES (?, ?, ?)",
                                [mission['id'], fileForThisMission, date.today()])

                        c.execute("UPDATE versions SET existsOnMM = 1 WHERE name = ?", [fileForThisMission])

            c.connection.commit()
            c.connection.close()

            c = utils.getCursor()

            fileNames = os.listdir(utils.missionMainDir)

            filesGroupedByMissionName = {}
            for k, g in itertools.groupby(fileNames, lambda x: SyncHandler.sanatizeFileName(self, x)):
                filesGroupedByMissionName[k] = list(g)

            c.execute('''SELECT name FROM versions''')
            versionRows = c.fetchall()
            versions = [x['name'] for x in versionRows]

            # for each db mission
            # find all files that match
            # for each file
            # find out if file is in db
            # if not
            # add to db
            for mission in missions:
                sanitizedName = SyncHandler.sanatizeMissionName(self, mission['missionName'])
                if sanitizedName in filesGroupedByMissionName:

                    filesForThisMission = filesGroupedByMissionName[sanitizedName]
                    for fileForThisMission in filesForThisMission:
                        if not fileForThisMission in versions:
                            c.execute(
                                "INSERT INTO versions(missionId, name, createDate, existsOnMM) VALUES (?, ?, ?, ?)",
                                [mission['id'], fileForThisMission, date.today(), False])
                        c.execute("UPDATE versions SET existsOnMain = 1 WHERE name = ?", [fileForThisMission])

            c.connection.commit()
            c.connection.close()


        else:
            start_response("403 Permission Denied", [])
            return ["Access Denied".encode()]

        start_response("200 OK", [])
        return []

    def getHandled(self):
        return "sync"

    def sanatizeFileName(self, x: str):
        x = x.replace('fa3_', '')
        x = re.sub(r'(a|c|z|x|w|r)+\d+', "", x)
        x = re.sub(r'v(t)*\d+.*', "", x)
        x = x.replace("_", "")
        x = x.lower()
        return x

    def sanatizeMissionName(self, x: str):
        x = x.lower()
        x = x.replace(' ', '')
        x = x.replace('\'', '')
        x = x.replace('(', '')
        x = x.replace(')', '')
        x = x.replace('/', '')
        return x
