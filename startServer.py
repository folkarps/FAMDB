import os
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

import utils
from saveMission import handleSaveMission

c = utils.getCursor()
missionMakerDir = ''
missionMainDir = ''
missionMainArchive = ''
missionMakerArchive = ''

# Create table
c.execute('''CREATE TABLE if not exists missions
             (id integer primary key,
              missionName text,
              lastPlayed text,
               missionAuthor text,
              missionModified text,
              framework text,
               isBroken integer default 0,
              needsRevision integer default 0,
               missionPlayers int,
               missionType text,
               missionMap text,
                playedCounter int default 0,
                missionDesc text,
                missionNotes text)''')

c.execute('''CREATE TABLE if not exists users
             (id integer primary key, login text, email text, password text, createDate text, lastLogin text, permissionLevel integer)''')
# Create table
c.execute('''CREATE TABLE if not exists versions
             (id integer primary key, missionId integer, existsOnMM integer default 1, existsOnMain integer default 0, name text, createDate text, toBeArchivedMM integer default 0, toBeDeletedMM integer default 0, toBeDeletedMain integer default 0, toBeArchivedMain default 0)''')

c.execute('''CREATE TABLE if not exists comments
             (id integer primary key, contents text, user text, createDate text, missionId integer)''')

c.execute('''CREATE TABLE if not exists sessions
             (id integer primary key, missionNames text, date text, host text, name text, players integer)''')

# Save (commit) the changes
c.connection.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
c.connection.close()

from deleteVersion import handleVersionDelete
from cleanup import handleCleanup
from createUser import handleCreateUser
from login import handleLogin
from authors import handleAuthors
from editSession import handleEditSession
from deleteMission import handleMissionDelete
from deleteSession import handleSessionDelete
from session import handleGetSession
from archive import handleArchive
from move import handleMove
from missions import handleMissions
from users import handleUsers
from setPermissionLevel import handlePermissionLevel
from upload import handleUpload
from urllib.parse import urlparse

# add each of the path handlers to the pathHandler map

pathHandlers = {'missions': handleMissions, 'authors': handleAuthors, 'users': handleUsers,
                'sessions': handleGetSession}

postHandlers = {'deleteVersion': handleVersionDelete, 'login': handleLogin, 'signup': handleCreateUser,
                'move': handleMove, 'archive': handleArchive, 'cleanup': handleCleanup, 'upload': handleUpload,
                'saveMission': handleSaveMission, "setPermissionLevel": handlePermissionLevel,
                "editSession": handleEditSession, "deleteSession": handleSessionDelete,
                "deleteMission": handleMissionDelete}


# HTTPRequestHandler class
class mainRequestHandler(SimpleHTTPRequestHandler):
    # GET
    def do_GET(self):
        o = urlparse(self.path)
        path = str.replace(o.path, "/", "")
        if path in pathHandlers:
            pathHandlers[path](self)
        else:
            super().do_GET()
        return

    def do_POST(self):
        o = urlparse(self.path)
        path = str.replace(o.path, "/", "")
        if path in postHandlers:
            postHandlers[path](self)
        return

    def log_message(self, format, *args):
        print("%s - - [%s] %s" %
              (self.address_string(),
               self.log_date_time_string(),
               format % args))
        return


def run():
    print('starting server...')

    # Server settings
    server_address = ('', utils.port)
    httpd = HTTPServer(server_address, mainRequestHandler)

    path = Path("famdb.pid")
    if path.exists():
        file = open("famdb.pid", "r")
        pid = int(list(file)[0])
        serverRunning = utils.isPidRunning(pid)
        if serverRunning:
            print('Fatal:Detecting server already running as pid:' + str(pid) + "\nPlease kill this first",
                  file=sys.stderr)
            return
        else:
            print('Warning:PID file detected, but no running process found, continuing')
    file = open("famdb.pid", "w+")
    file.write(str(os.getpid()))
    file.close()

    print('running server...')
    httpd.serve_forever()


run()
