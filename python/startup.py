import sqlite3
from http.server import HTTPServer, SimpleHTTPRequestHandler

conn = sqlite3.connect('famdb.db')
missionMakerDir = ''
missionMainDir = ''
missionMainArchive = ''
missionMakerArchive = ''
c = conn.cursor()

# Create table
c.execute('''CREATE TABLE if not exists missions
             (id integer primary key,
              missionName text,
              lastPlayed text,
               missionAuthor text,
              missionModified text,
               isBroken integer,
              needsRevision integer,
               missionPlayers int,
               missionType text,
               missionMap text,
                playedCounter int,
                missionDesc text,
                missionNotes text)''')
c.execute('''insert into missions(name, lastPlayed, missionAuthor, missionModified, isBroken, needsRevision, missionPlayers, missionType, missionMap, playedCounter, missionDesc, missionNotes)
                values ('test name', '2016-08-16', 'test author', '2016-01-01', 0, 0, 11, 'Cooperative', 'Altis', 5, 'test description', 'test Notes')''')

c.execute('''CREATE TABLE if not exists users
             (id integer primary key, name text, email text, password text, createDate text, lastLogin text, permissionLevel integer)''')
# Create table
c.execute('''CREATE TABLE if not exists versions
             (id integer primary key, origin text, missionId integer, name text, createDate text, toBeArchived integer, toBeDeleted integer)''')

c.execute('''CREATE TABLE if not exists comments
             (id integer primary key, contents text, user text, createDate text, missionId integer)''')

# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()

from delete import handleDelete
from cleanup import handleCleanup
from archive import handleArchive
from move import handleMove
from missions import handleMissions
from urllib.parse import urlparse

# add each of the path handlers to the pathHandler map

pathHandlers = {'missions': handleMissions, 'delete': handleDelete,
                'move': handleMove, 'archive': handleArchive, 'cleanup': handleCleanup}


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


def run():
    print('starting server...')

    # Server settings
    # Choose port 8080, for port 80, which is normally used for a http server, you need root access
    server_address = ('127.0.0.1', 8080)
    httpd = HTTPServer(server_address, mainRequestHandler)
    print('running server...')
    httpd.serve_forever()


run()
