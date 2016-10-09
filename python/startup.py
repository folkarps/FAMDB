from http.server import HTTPServer, SimpleHTTPRequestHandler

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
               isBroken integer,
              needsRevision integer,
               missionPlayers int,
               missionType text,
               missionMap text,
                playedCounter int,
                missionDesc text,
                missionNotes text)''')

c.execute('''CREATE TABLE if not exists users
             (id integer primary key, login text, email text, password text, createDate text, lastLogin text, permissionLevel integer)''')
# Create table
c.execute('''CREATE TABLE if not exists versions
             (id integer primary key, missionId integer, existsOnMM integer default 1, existsOnMain integer default 0, name text, createDate text, toBeArchivedMM integer default 0, toBeDeletedMM integer default 0, toBeDeletedMain integer default 0, toBeArchivedMain default 0)''')

c.execute('''CREATE TABLE if not exists comments
             (id integer primary key, contents text, user text, createDate text, missionId integer)''')

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
from archive import handleArchive
from move import handleMove
from missions import handleMissions
from upload import handleUpload
from urllib.parse import urlparse

# add each of the path handlers to the pathHandler map

pathHandlers = {'missions': handleMissions, 'authors': handleAuthors}

postHandlers = {'deleteVersion': handleVersionDelete, 'login': handleLogin, 'signup': handleCreateUser,
                'move': handleMove, 'archive': handleArchive, 'cleanup': handleCleanup, 'upload': handleUpload,
                'saveMission': handleSaveMission}


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


def run():
    print('starting server...')

    # Server settings
    # Choose port 8080, for port 80, which is normally used for a http server, you need root access
    server_address = ('127.0.0.1', 8080)
    httpd = HTTPServer(server_address, mainRequestHandler)
    print('running server...')
    httpd.serve_forever()


run()
